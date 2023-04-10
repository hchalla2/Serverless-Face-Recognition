#include<bits/stdc++.h>
using namespace std;

int is_possible(vector<int> execution_times, int x, int y, int operations)
{
    int diff = x - y;
    vector<int> new_exe;
    int i,sz = execution_times.size();
    for(i=0;i<sz;i++)
    {
        new_exe.push_back(execution_times[i] - operations * y;)
    }

    for(i=0;i<sz;i++)
    {
        if(new_exe[i]>0)
        {
            req = req + (execution_times[i])/x;
        }
        if(execution_times[i]%x==0)
            req++;
    }


    if(req<=operations)
        return true;
    else
        return false;

}

int binary_search(vector<int> execution_times, int x,int y)
{
    int l = 1, r = 10000000;
    while(l<=r)
    {
        if(!is_possible(execution_times, x, y, mid) && is_possible(execution_times, x,y, mid+1))
        {
            return mid+1;
        }
        else if(!is_possible(execution_times, x, y, mid) && !is_possible(execution_times, x,y, mid+1))
        {
            l = mid + 1;
        }
        else 
        {
            r = mid -1;
        }
    }
    return -1;
}

int main()
{
    int n;
    cin >> n; 

    

    int x,y;
    cin >> x >> y;


    return 0;
}