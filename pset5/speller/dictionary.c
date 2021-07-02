// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 50000;

// Hash table
node *table[N];
int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int word_index = hash(word);
    node *cursor = table[word_index];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor=cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Function should take a string and return an index
    // This hash function adds the ASCII values of all characters in the word together
    long sum = 0;    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *fptr = fopen(dictionary, "r");
    
    if (fptr == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return false;
    }
    
    char loaded_word[LENGTH + 1];
    
    while (fscanf(fptr, "%s", loaded_word) != EOF)
    {
        //allocate memory for node
        node *n = malloc(sizeof(node));
        
        if (n == NULL)
        {
            return false;
        }
        //copy loaded word to node
        strcpy(n->word, loaded_word);
        //get table index from hash function
        int index = hash(loaded_word);
        //insert node in front of the list on the specific hash index
        n->next = table[index];
        //update the list to point at the added node
        table[index] = n;
        dict_size++;
    }
    fclose(fptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i<N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        if (cursor == NULL && i == N-1)
        {
            return true;
        }
    }
    return false;
}
