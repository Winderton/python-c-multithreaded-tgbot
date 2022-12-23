#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>


int* allocate(int N)
{
    int* ptr = (int*)malloc(sizeof(int) * N);

    if (ptr != NULL)
    {
        for (int i = 0; i < N; i++)
        {
            ptr[i] = 0;
        }
    }

    return ptr;
}


int* generate(int N)
{
    int* ptr = allocate(N);
    
    if (ptr != NULL)
    {
        for (int i = 0; i < N; i++)
        {
            ptr[i] = i;
        }
    }

    return ptr;
}



int binary_search_impl(int x)
{
    int left = 0;
    int arrSize = INT_MAX / 32;
    int right = arrSize - 1;

    int* arr = generate(arrSize);

    printf("Start searching\n");

    while(left <= right)
    {
        int mid = left + (right - left) / 2;
        if (arr[mid] == x)
        {
            printf("Found\n");
            free(arr);
            return mid;
        }
        if (arr[mid] < x)
        {
            left = mid +1;
        }

        else
        {
            right = mid - 1;
        }
    }   
    
    free(arr);
    return -1;
}


float pi_impl(long S)
{
    float sum = 0.0, sample;

    for (long i = 0; i < S; i++)
    {
        sample = pow(-1, i) / (2 * i +1);
        sum += sample;
    }

    printf("pi=%.6f\n", 4 * sum);
    return 4 * sum;
}

