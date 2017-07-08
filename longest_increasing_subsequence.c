#include <stdio.h>
#include <stdlib.h>

int lis(int a[],int n){
    int *lis,i,j,max=0;
    lis = (int*)malloc(sizeof(int) * n);
    for(i=0;i<n;i++)
        lis[i] = 1;
    for(i=1;i<n;i++){
        for(j=0;j<i;j++){
            if(a[i] > a[j] && lis[i] < lis[j] + 1)
                lis[i] = lis[j] + 1;
        }
    }
    for(i = 0 ; i < n ; i++)
        if(max < lis[i])
            max = lis[i];
    free(lis);
    return max;
}

int main() {
	//code
	int t,i,n,a[1000];
	scanf("%d",&t);
	while(t--){
	    scanf("%d",&n);
	    for(i = 0 ; i < n ; i++)
	        scanf("%d",&a[i]);   
	    printf("%d\n",lis(a,n));
	}
	return 0;
}
