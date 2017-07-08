#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int min(int a,int b,int c){
	if(a < b)
		return (a<c) ? a : c;
	else
		return (b<c) ? b : c;
}

int minCost(int a[3][3],int n,int m){
	if(n < 0 || m < 0)
		return INT_MAX;
	if(n == 0 && m == 0)
		return a[n][m];
	else
		return a[n][m] + min(minCost(a,n-1,m) , minCost(a,n,m-1) , minCost(a,n-1,m-1));	
}

int main(){
	int a[3][3];
	int i,j,n,m;
	
	scanf("%d%d",&n,&m);
	
	for(i = 0 ; i < n ; i++){
		for(j = 0 ; j < m ; j++){
			scanf("%d",&a[i][j]);
		}
	}
	
	printf("Minimum cost is : %d",minCost(a,n,m));	
	
	return 0;
}
