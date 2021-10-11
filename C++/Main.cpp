// Phases are in Q1.63 format and are specified in turns
// Output is in Q2.63 format 

#include <cmath>

#include <future>
#include <queue>

#include <bitset>
#include <iomanip>
#include <iostream>

import Benchmark;


constexpr unsigned input[]  = {4, 32};
constexpr unsigned output[] = {4, 32};

int main()
{
    std::queue<std::future<SinCosResult>> future;
    
    for (unsigned i = input[0]; i <= input[1]; i++)
        for (unsigned o = input[0]; o <= input[1]; o++)
            future.push(std::async(std::launch::async, benchmarkSinCos, i, o));

    std::cout << "input bits,output bits,mean,standard deviation,min error,max error\n";

    for (unsigned i = input[0]; i <= input[1]; i++)
        for (unsigned o = input[0]; o <= input[1]; o++)
        {
            future.front().wait();
            auto result = future.front().get();

            future.pop();

            std::cout << i << ",";
            std::cout << o << ",";
            std::cout << result.mean_ << ",";
            std::cout << result.sd_ << ",";
            std::cout << result.min_ << ",";
            std::cout << result.max_ << "\n";
        }

    return 0;
}
