#ifndef MYLIB_H
#define MYLIB_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize the mylib library
 * @return 0 on success, -1 on error
 */
int mylib_init(void);

/**
 * @brief Simple addition function
 * @param a First number
 * @param b Second number
 * @return Sum of a and b
 */
int mylib_add(int a, int b);

/**
 * @brief Simple string processing function
 * @param str Input string
 * @return Length of processed string
 */
int mylib_process_string(const char * str);

#ifdef __cplusplus
}
#endif

#endif // MYLIB_H