#include <stdio.h>
#include <string.h>
#include <stdlib.h>


//this method uses top down approach of dynamic programming
int string_total_count(char *s,char *find,int slen,int findlen){
	int result = 0,dp[findlen+1][slen+1],i,j,k;
	for(i = 0 ; i <= findlen ; i++){
		for(j = 0 ; j <= slen ; j++){
			if(j < i || i == 0 || j == 0){
				dp[i][j] = 0;
			}
			else if(find[i-1] == s[j-1]){
				k = dp[i][j-1] + dp[i-1][j-1];
				if((k == 0 && j == i) || i == 1){
					dp[i][j] = k + 1;
				}else{
					dp[i][j] = dp[i][j-1] + dp[i-1][j-1];
				}
			}
			else{
				dp[i][j] = dp[i][j-1];
			}
		}
	}
	return dp[findlen][slen];
}

int main()
{
	char s[100],find[100];
	int t;
	scanf("%d",&t);
	while(t--){
		scanf("%s",s);
		scanf("%s",find);
		printf("%d",string_total_count(s,find,strlen(s),strlen(find)));
		printf("\n");
	}
	return 0;
}
