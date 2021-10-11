// Phase is in Q1.63 / 4 ((1 sign bit + 63 fraction bits) divided by 4)

module;

#include <cassert>
#include <cmath>

#include <numbers>
#include <vector>

export module Lut;


export struct Lut
{
    Lut(unsigned inputBits, unsigned outputBits);

    const unsigned inputBits_;
    const unsigned outputBits_;

    std::vector<long long> angle_;
    long long k_;
};


Lut::Lut(const unsigned inputBits, unsigned outputBits) :
inputBits_(inputBits),
outputBits_(outputBits)
{
    assert(inputBits  >= 4 && inputBits  <= 64);
    assert(outputBits >= 4 && outputBits <= 64);

    double power{0.};
    double product{1.};

    long long inputMask  = static_cast<long long>(0xFFFF'FFFF'FFFF'FFFFULL << (64 - inputBits));
    long long outputMask = static_cast<long long>(0xFFFF'FFFF'FFFF'FFFFULL << (64 - outputBits));

    while (true)
    {
        double radian = std::atan(std::pow(2., -power));
        long long turn = (static_cast<long long>(radian * 0x1p65 / std::numbers::pi) + (1LL << (63 - inputBits))) & inputMask;

        if (turn)
        {
            if (power)
                angle_.push_back(turn);

            product *= std::cos(radian);
        }
        else
            break;

        power++;
    }

    k_ = (long long(product * 0x1p62) + (1LL << (63 - outputBits))) & outputMask;
}
