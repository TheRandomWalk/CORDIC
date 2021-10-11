module;

#include <cmath>

#include <tuple>

export module Cordic;

export import Lut;


export auto sinCos(long long x, const Lut& lut) -> std::tuple<long long, long long>
{
    unsigned long long ux = x;

    long long sin = 0;
    long long cos = 0;

    switch (ux >> 62)
    {
    case 0b00:   // ( 0/2 pi, +1/2 pi)
    {
        sin = +lut.k_;
        cos = +lut.k_;
        x -= 0x2000'0000'0000'0000LL;
        break;
    }

    case 0b01:   // (+1/2 pi, +2/2 pi)
    {
        sin = +lut.k_;
        cos = -lut.k_;
        x -= 0x6000'0000'0000'0000LL;
        break;
    }

    case 0b10:   // (-2/2 pi, -1/2 pi)
    {
        sin = -lut.k_;
        cos = -lut.k_;
        x += 0x6000'0000'0000'0000LL;
        break;
    }

    case 0b11:   // (-1/2 pi, 0/2 pi)
    {
        sin = -lut.k_;
        cos = +lut.k_;
        x += 0x2000'0000'0000'0000LL;
        break;
    }
    }

    x <<= 2;

    long long newSin;
    long long newCos;

    long long mask = static_cast<long long>(0xFFFF'FFFF'FFFF'FFFFULL << (64 - lut.outputBits_));

    unsigned nIteration = std::min(static_cast<unsigned>(lut.angle_.size()), lut.outputBits_ - 1);

    for (unsigned iteration = 0; iteration < nIteration; iteration++)
    {
        if (x >= 0)
        {
            newSin = sin + ((cos >> (iteration + 1)) & mask);
            newCos = cos - ((sin >> (iteration + 1)) & mask);
            x -= lut.angle_[iteration];
        }
        else
        {
            newSin = sin - ((cos >> (iteration + 1)) & mask);
            newCos = cos + ((sin >> (iteration + 1)) & mask);
            x += lut.angle_[iteration];
        }

        sin = newSin;
        cos = newCos;
    }

    return {sin, cos};
}
