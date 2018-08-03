
/*
 * Copyright (c) 2015-2018 Agalmic Ventures LLC (www.agalmicventures.com)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

#include <cstdint>
#include <cstdio>
#include <cstdlib>

static inline uint64_t rdtscp(uint32_t &aux)
{
	uint64_t tsc;
	asm volatile (
		//A is EDX:EAX
		"rdtscp\n" : "=A" (tsc), "=c" (aux) : :
	);
	return tsc;
}

int main()
{
	uint32_t core;
	uint32_t lastCore = 0xFFFF;
	uint64_t lastTime = 0;

	while (true) {
		uint64_t time = rdtscp(core);
		if (core != lastCore) {
			std::printf("%u -> %u (TSC = %llu = %llu + %llu)\n",
				lastCore, core,
				time, lastTime, time - lastTime);
			lastCore = core;
			lastTime = time;
		}
	}
}
