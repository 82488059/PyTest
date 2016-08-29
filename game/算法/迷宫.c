#define MAZE_MAX    50
char map[MAZE_MAX+2][MAZE_MAX+2];
int search(int x,int y)
{
    static int d[4][2]={0,1,1,0,0,-1,-1,0};
    int zx=x*2,zy=y*2,next,turn,i;
    map[zx][zy]=1; turn=rand()%2? 1:3;
    for(i=0,next=rand()%4;i<4;i++,next=(next+turn)%4)
        if(map[zx+2*d[next][0]][zy+2*d[next][1]]==0)
            map[zx+d[next][0]][zy+d[next][1]]=1,
            search(x+d[next][0],y+d[next][1]);
    return 0;
}
void Make_Maze(int x,int y)
{
    int z1,z2;
    for(z1=0,z2=2*y+2;z1<=2*x+2;z1++)
        map[z1][0]=1,map[z1][z2]=1;
    for(z1=0,z2=2*x+2;z1<=2*y+2;z1++)
        map[0][z1]=1,map[z2][z1]=1;
    map[1][2]=1;map[2*x+1][2*y]=1;
    srand((unsigned)time(NULL));
    search(rand()%x+1,rand()%y+1);
}
int main(void)
{
    int x=8,y=8,z1,z2; //x和y的值指定了这个要生成的迷宫的大小
    Make_Maze(x,y);
    for(z2=1;z2<=y*2+1;z2++){
        for(z1=1;z1<=x*2+1;z1++) fputs(map[z1][z2]?"　":"█",stdout);
        if(z2<=y*2)putchar(10);
    }
    return 0;
}