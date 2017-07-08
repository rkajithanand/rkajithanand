#include <stdio.h>
#include <string.h>

int max(int i,int j)
{
    return (i>j)?i:j;
}

int lcs(char* first, char* second,int row,int col){
    int lcs[row+1][col+1],i,j,k;
    for(i = 0 ; i <= row ; i++){
        for(j = 0 ; j <= col ; j++){
            if( i == 0 || j == 0)
                lcs[i][j] = 0;
            else if(first[i-1] == second[j-1]){
                k = lcs[i-1][j-1] + 1;
            	if(k == 1)
            		lcs[i][j] = k;
            	else{
            		if(first[i-2] == second[j-2])
            			lcs[i][j] = lcs[i-1][j-1] + 1;
            		else
            			lcs[i][j] = max(lcs[i-1][j],lcs[i][j-1]);
				}
			}
            else
                lcs[i][j] = max(lcs[i-1][j],lcs[i][j-1]);
        	printf("%d ",lcs[i][j]);
		}
		printf("\n");
    }
    return lcs[row][col];
}

int main() {
	//code
	int t,row,col;
	char first[100],second[100];
	scanf("%d",&t);
	while(t--){
	    scanf("%d%d",&row,&col);
	    scanf("%s",first);
	    scanf("%s",second);
	    printf("%d\n",lcs(first,second,row,col));
	}
	return 0;
}
