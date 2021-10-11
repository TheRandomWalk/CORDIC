module;

#include <cmath>

#include <numbers>
#include <tuple>

export module Benchmark;

export import Cordic;


export struct SinCosResult
{
    double mean_{0};
    double sd_{0};
    double min_{+2};
    double max_{-2};
};


export auto benchmarkSinCos(unsigned inputBits, unsigned outputBits) -> SinCosResult
{
    Lut lut(inputBits, outputBits);
    
    SinCosResult result;

    double square{0};
    double cosSquare{0};

    unsigned long long n{ 1ULL << inputBits };

    for (unsigned long long u{0}; u < n; u++)
    {
        long long s = static_cast<long long>(u << (64 - inputBits));
        auto [sin, cos] = sinCos(s, lut);

        double sinCordic = static_cast<double>(sin) / 0x1p62;
        double sinTrue = std::sin(static_cast<double>(s) * std::numbers::pi / 0x1p63);

        double cosCordic = static_cast<double>(cos) / 0x1p62;
        double cosTrue = std::cos(static_cast<double>(s) * std::numbers::pi / 0x1p63);

        double sinError = sinCordic - sinTrue;
        double cosError = cosCordic - cosTrue;

        result.mean_ += sinError + cosError;
        
        square += sinError * sinError + cosError * cosError;

        result.min_ = std::min(result.min_, sinError);
        result.min_ = std::min(result.min_, cosError);

        result.max_ = std::max(result.max_, sinError);
        result.max_ = std::max(result.max_, cosError);
    }

    result.mean_ /= n << 1;
    
    square /= n << 1;

    result.sd_ = std::sqrt(square - result.mean_ * result.mean_);

    return result;
}
