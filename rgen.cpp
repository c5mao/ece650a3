// adapted from https://www.gnu.org/software/libc/manual/html_node/Example-of-Getopt.html
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>
using namespace std;

#define MAX_NUM 4294967295

/// main() must be declared with arguments
/// otherwise command line arguments are ignored
int main (int argc, char **argv)
{
    string cvalue;
    int c;
    int sk=10;
    int nk=5;
    int lk=5;
    int ck=20;
    int error=0; //0 for no error, graph generate succeed, 1 for error after try 25 times
    unsigned int num;
    unsigned int sk_num;

    opterr = 0;


    ifstream urandom("/dev/urandom");

    // expected options are '-s value', '-n value', '-l value',and '-c value'
    while ((c = getopt (argc, argv, "s:n:l:c:")) != -1)
        switch (c)
        {
        case 's':
            cvalue = optarg;
            sk = atoi(cvalue.c_str());
            break;
        case 'n':
            cvalue = optarg;
            nk = atoi(cvalue.c_str());
            break;
        case 'l':
            cvalue = optarg;
            lk = atoi(cvalue.c_str());
            break;
        case 'c':
            cvalue = optarg;
            ck = atoi(cvalue.c_str());
            break;
        case '?':
            cerr << "Error: unknown option" << endl;
            return 1;
        default:
            return 0;
        };

    unsigned int *street_edges = new unsigned int[(unsigned int)sk];



	while(1){
    	urandom.read((char*)&num, sizeof(int));
    	sk_num = (float)num*(sk-2)/MAX_NUM+2;
    	unsigned int *new_street_edges = new unsigned int[sk_num];
    	delete [] street_edges;
    	street_edges = new_street_edges;
    	unsigned int total_v=0;
    	unsigned int m=0,n=0,i=0,j=0,count=0;
    	unsigned int index=0,index1=0,index2=0,offset1=0,offset2=0;
    	float x1=0,x2=0,x3=0,x4=0,y1=0,y2=0,y3=0,y4=0;
    	float xnum=0, xden=0; 
    	bool overlap_error=0;

    	//total vertices = summation of each (street edges plus 1)
    	for (m=0; m<sk_num ; m++){
        	urandom.read((char*)&num, sizeof(int));
        	//cout<<num<<endl;
        	street_edges[m]= (float)num*(nk-1)/MAX_NUM+1;
        	//cout<<street_edges[m]<<endl;
        	total_v=total_v+street_edges[m]+1;
    	}
    	//cout<<"total vertices:"<<total_v<<endl;
    	int x[total_v];
    	int y[total_v];

		do{
    		//generate random vertices with coordinates
    		for (m=0 ; m<total_v ; m++){
        		urandom.read((char*)&num, sizeof(int));
        		x[m]=(float)num*2*ck/(unsigned int)MAX_NUM-ck;
        		urandom.read((char*)&num, sizeof(int));
        		y[m]=(float)num*2*ck/(unsigned int)MAX_NUM-ck;
        		//cout << '(' << x[m] << ',' << y[m] << ')' <<endl;
   			}

    		index1=0,index2=0,offset1=0,offset2=0;
    		x1=0,x2=0,x3=0,x4=0,y1=0,y2=0,y3=0,y4=0;
    		xnum=0, xden=0; 
    		overlap_error=0;
    		offset1=street_edges[0];
    		offset2=street_edges[0];
    		for (m=0;m<total_v-1;m++){
       			if (overlap_error==1)
        	    	break;
        		x1=(float)x[m];
        		x2=(float)x[m+1];
        		y1=(float)y[m];
        		y2=(float)y[m+1];
        		if (m==offset1-1){
            		offset1=offset1+street_edges[index1];
            		index1++;
        		}else{
            		for(n=m+1;n<total_v-1;n++){
                		x3=(float)x[n];
                		x4=(float)x[n+1];
                		y3=(float)y[n];
                		y4=(float)y[n+1];
                
                		if (n==offset2-1){
                    		offset2=offset2+street_edges[index2];
                    		index2++;
                		}else{
                    		xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4));
                    		xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4));
                    		//check for overlapping
                    		if (abs(xnum)<=0.01 && abs(xden)<=0.01){
                        		if ((abs(x1-x2)<=0.01 && abs(y1-y2)<=0.01) || (abs(x3-x4)<=0.01 && abs(y3-y4)<=0.01)){
                            		overlap_error=1;//two vertices are the same
                            		break;
                        		}
                        		if (abs(max(max(x1,x2),max(x3,x4))-min(min(x1,x2),min(x3,x4))-abs(x1-x2)-abs(x3-x4))<=0.01){
                            		overlap_error=0;//intersect with one edge vertex
                        		}
                        		if (max(max(x1,x2),max(x3,x4))-min(min(x1,x2),min(x3,x4)) < abs(x1-x2)+abs(x3-x4)){
                            		overlap_error=1;//overlapping
                            		break;
                        		}
                    		}
                		}               
            		}
        		}
    		}
    		count++;
    		if (count>=25){
        		error=1;
       			break;
    		}
		}while(overlap_error);

    	if (error){
    		cout << "r" << endl;
    		cout << "g" << endl;
    	}
		else{
			cout << "r" << endl;
        	index=0;
    		if (!error){
        		for (i=0;i<sk_num;i++){
            		cout << "a \"" << i << "\""; 
            		for (j=0;j<street_edges[i]+1;j++){
                		cout << " (" << x[index+j] << "," << y[index+j] << ")" ;     
            		}
            		index=index+street_edges[i]+1;
            		cout << endl;
       			}
    		}
    		cout << "g" << endl;
		}  
	    //put a delay to regenerate the graph again 
    	unsigned int wait_seconds;
    	urandom.read((char*)&num, sizeof(int));
    	wait_seconds= (float)num*(lk-5)/MAX_NUM+5;
    	sleep(wait_seconds);	
	}

    return 0;
}
