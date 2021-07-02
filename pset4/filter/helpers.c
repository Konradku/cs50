#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int i,j;
    for (i=0; i<height; i++)
    {
        for (j=0; j<width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue)/3);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int i,j;
    for (i=0; i<height; i++)
    {
        for (j=0; j<width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed > 255) sepiaRed = 255;
            if (sepiaGreen > 255) sepiaGreen = 255;
            if (sepiaBlue > 255) sepiaBlue = 255;
            
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int i,j;
    for (i=0; i<height; i++)
    {
        for (j=0; j<width/2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width-(j+1)];
            image[i][width-(j+1)] = temp;         
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int i,j;
    RGBTRIPLE temp[height][width];
    for (i=0; i<height; i++)
    {
        for (j=0; j<width; j++)
        {
            temp[i][j] = image[i][j];
        }    
    }
    
    for (i=0; i<height; i++)
    {
        for(j=0; j<width; j++)
        {
            int sum_red = 0;
            int sum_green = 0;
            int sum_blue = 0;
            int counter = 0;
            int k,l;
            
            for (k=-1; k<2; k++)
            {
                for (l=-1; l<2; l++)
                {
                    if (i+k<0 || i+k>=height) continue;
                    if (j+l<0 || j+l>=width) continue;
                    
                    sum_red += temp[i+k][j+l].rgbtRed;
                    sum_green += temp[i+k][j+l].rgbtGreen;
                    sum_blue += temp[i+k][j+l].rgbtBlue;
                    counter++;
                }
            }
        image[i][j].rgbtRed = round(sum_red/counter);
        image[i][j].rgbtGreen = round(sum_green/counter);
        image[i][j].rgbtBlue = round(sum_blue/counter);
        }
    }
    return;
}
