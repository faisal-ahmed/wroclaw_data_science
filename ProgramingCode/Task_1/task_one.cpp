#include<stdio.h>

// SQRT of 17179869181 131071

using LL = long long int;
#define MAX_SQRT 131075 // 131075 needed For detecting prime upto 2^34
#define MAX_10_DIGIT_NUMBER 9999999999LL
#define MIN_10_DIGIT_NUMBER 1000000000LL
#define MAX_8_DIGIT_NUMBER 99999999LL
#define MIN_8_DIGIT_NUMBER 10000000LL
#define MAX_6_DIGIT_NUMBER 999999LL
#define MIN_6_DIGIT_NUMBER 100000LL
#define MAX_ZERO_10_DIGIT 32
#define MIN_ZERO_10_DIGIT 28
#define MAX_ZERO_8_DIGIT 25
#define MIN_ZERO_8_DIGIT 22
#define MAX_ZERO_6_DIGIT 18
#define MIN_ZERO_6_DIGIT 15

LL primes[12300]; //12251

bool isPrime(LL n){
    LL i;
    for (i = 0; (primes[i] * primes[i]) <= n; i++) if (!(n % primes[i])) return false;
    return true;
}

void generatePrime(){
    primes[0] = 2;
    bool matrix[MAX_SQRT] = {false};
    LL i, j;
    
    for (i = 3; i < MAX_SQRT; i += 2)
        if (!matrix[i])
            for (j = i*i; j < MAX_SQRT; j += (2*i)) matrix[j] = 1;

    for (i = 3, j = 1; i < MAX_SQRT; i += 2) if (!matrix[i]) primes[j++] = i;
}

LL findPrimes(int numberOfZero, long long int max_number, long long int min_number){
    LL outputMax = 0;

    int zeroCount, zeroSliderAt, i;
    for (zeroCount = 1; zeroCount <= numberOfZero; zeroCount++){
        //LSB and MSB are always 1
        //Zero slides start after LSB, from right to left
        for (zeroSliderAt = 1; zeroSliderAt < (numberOfZero+2-zeroCount); zeroSliderAt++){
            //newNumber all 1 bit number
            LL newNumber = (1LL<<(numberOfZero+2))-1, zeroOffset = 0;
            for (i = 0; i < zeroCount; i++){
                zeroOffset ^= (1LL<<(zeroSliderAt+i));
            }
            newNumber ^= zeroOffset;

            if (newNumber < max_number && newNumber > min_number && isPrime(newNumber)) {
                if (newNumber > outputMax) outputMax = newNumber;
                //bitset<numeric_limits<unsigned long long>::digits> b(outputMax);
                //cout << "It's binary representation is " << b << endl;
            }
        }
    }

    return outputMax;
}

int main() {
    generatePrime();
    LL desiredPrime;
    int i;
    //for 10 digits
    for (i = MAX_ZERO_10_DIGIT; i >= MIN_ZERO_10_DIGIT; i--){
        desiredPrime = findPrimes(i, MAX_10_DIGIT_NUMBER, MIN_10_DIGIT_NUMBER);
        if (desiredPrime) {
            printf ("For 10 digits: %lld\n", desiredPrime);
            break;
        }
    }

    //for 8 digits
    for (i = MAX_ZERO_8_DIGIT; i >= MIN_ZERO_8_DIGIT; i--){
        desiredPrime = findPrimes(i, MAX_8_DIGIT_NUMBER, MIN_8_DIGIT_NUMBER);
        if (desiredPrime) {
            printf ("For 8 digits: %lld\n", desiredPrime);
            break;
        }
    }

    //for 6 digits
    for (i = MAX_ZERO_6_DIGIT; i >= MIN_ZERO_6_DIGIT; i--){
        desiredPrime = findPrimes(i, MAX_6_DIGIT_NUMBER, MIN_6_DIGIT_NUMBER);
        if (desiredPrime) {
            printf ("For 6 digits: %lld\n", desiredPrime);
            break;
        }
    }

    return 0;
}