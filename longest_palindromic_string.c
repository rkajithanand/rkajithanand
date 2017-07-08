#include <stdio.h>
#include <string.h>

int max(int a,int b){
	return a>b ? a : b;
}

int longest_palindromic_substring(char *s,int n){
	int dp[n+1][n+1],i,j,k;
	for( i= 0 ; i <= n ; i++){
		for( j = n, k = 0; j >= 0 ; j--,k++ ){
			if(i == 0 || k == 0)
				dp[i][k] = 0;
			else{
				if(s[i-1] == s[j]){
					dp[i][k] = dp[i-1][k-1] + 1;
				}
				else
					dp[i][k] = max(dp[i-1][k],dp[i][k-1]);
			}
		}
	}
	return dp[n][n];
}


int main(){
	char s[100];
	int t;
	scanf("%d",&t);
	while(t--){
		scanf("\n");
		scanf("%[^\n]s",s);
		printf("%d\n",longest_palindromic_substring(s,strlen(s)));
	}
	return 0;
}
