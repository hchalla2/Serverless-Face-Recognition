#include<bits/stdc++.h>
using namespace std;

int freq_map[100005][20];

int is_possible(int index, vector<int>& req)
{
    for(m=0;m<=9;m++)
    {
        if(freq_map[index]>req[m])
            return false;
    }
    return true;
}

int binary_search(vector<int>& temp)
{
    int l = 0, r = s.size()-1;
    while(l<=r)
    {   
        int mid = (l+r)/2;
        if(!is_possible(mid, temp) && is_possible(mid+1, temp))
            return (mid+1);
        else if(!is_possible(mid, temp) && !is_possible(mid+1, temp))
        {
            l = mid-1;
        }
        else
        {
            r = mid+1;
        }
    }
    return -1;
}

int main()
{
    int i,n;
    string s;
    for(i=1;i<sz;i++)
    {
        for(m=0;m<=9;m++)
        {
            freq_map[i][m]=freq_map[i-1][m];
        }
        freq_map[i][s[i]-48]++;
    }

    cin >> n;

    string arr[n+5];
    for(i=0;i<n;i++)
    {
        cin >> query;

        int query_sz = query.size();
        vector<int> temp;
        for(m=0;m<=9;m++)
        {
            temp.push_back(0);
        }
        for(i=0;i<query_sz;i++)
        {
            temp[query[i]-48]++;
        }
        cout << binary_search(temp) << endl;
    }

    

    return 0;
}