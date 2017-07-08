#include <stdio.h>
#include <string.h>

int subset_sum(int *a,int n,int sum){
	int dp[n+1][sum+1],i,j,temp;
	for(i = 0 ; i <= n ; i++){
		for(j = 0 ; j <= sum ; j++){
			if(j == 0){
				dp[i][j] = 1;	
			}else if(i == 0){
				dp[i][j] = 0;
			}else if(j < a[i-1]){
				dp[i][j] = dp[i-1][j];
			}else{
				dp[i][j] = dp[i-1][j] || dp[i-1][j-a[i-1]];
			}
		}
	}	
	
	return dp[n][sum];
}

int main(){
	int a[100],n,sum,i;
	scanf("%d",&n);
	for(i = 0 ; i < n ; i++)
		scanf("%d",&a[i]);
	scanf("%d",&sum);
	int ans = subset_sum(a,n,sum);
	if(ans == 1)
		printf("\nTrue");
	else
		printf("\nFalse");
	return 0;
}
