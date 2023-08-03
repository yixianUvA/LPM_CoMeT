/**
 * This header implements memory DTM using a low power mode.
 */

#ifndef __DRAM_STATICLOW_H
#define __DRAM_STATICLOW_H

#include <map>

#include "drampolicy.h"
#include "performance_counters.h"

class DramStaticLow : public DramPolicy {
public:
    DramStaticLow(
        const PerformanceCounters *performanceCounters,
        int numberOfBanks,
        float dtmCriticalTemperature,
        float dtmRecoveredTemperature,
        float off_bank_number);
    virtual std::map<int,int> getNewBankModes(std::map<int,int> old_bank_modes);

private:
    const PerformanceCounters *performanceCounters;
    unsigned int numberOfBanks;
    float dtmCriticalTemperature;
    float dtmRecoveredTemperature;
    float off_bank_number;
};

#endif
