#ifndef TIME_UTILS_HPP
#define TIME_UTILS_HPP

#include <boost/date_time/posix_time/posix_time.hpp>

typedef boost::posix_time::ptime Time;

class TimeUtils {

public:
    
    // Retorna o tempo corrente
    static Time getTime();
    // Retorna o tempo transcorrido entre beg e end
    static double elapsedSeconds(Time t1, Time t2);
    // Retorna o tempo transcorrido entre beg e agora
    static double elapsedSeconds(Time beg);
};




#endif
