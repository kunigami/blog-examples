#include "time_utils.hpp"

Time TimeUtils::getTime(){
    return boost::posix_time::microsec_clock::local_time();
}
double TimeUtils::elapsedSeconds(Time t1, Time t2){
    boost::posix_time::time_duration
        elapsed_time = (t1 < t2) ? t2-t1 : t1-t2;
    return elapsed_time.total_milliseconds()/1000.00;
}
double TimeUtils::elapsedSeconds(Time beg){
    Time now = getTime();
    return elapsedSeconds(beg, now);
}
