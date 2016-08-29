# -*- coding:utf-8 -*-
from random import randint

# #define MAZE_MAX    50
MAZE_MAX = 50

# char map[MAZE_MAX+2][MAZE_MAX+2];
map1 = {}
for x in xrange(0, MAZE_MAX + 2):
    map1[x] = {}
    for y in xrange(0, MAZE_MAX + 2):
        map1[x][y] = 0

# map[MAZE_MAX + 2][MAZE_MAX + 2]


# int search(int x,int y) {


def search(xx, yy):
    # static int d[4][2]={0,1,1,0,0,-1,-1,0};
    d = {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}, 2: {0: 0, 1: -1}, 3: {0: -1, 1: 0}}
    # int zx=x*2,zy=y*2,next,turn,i;
    zx = xx * 2
    zy = yy * 2
    # map[zx][zy]=1; turn=rand()%2? 1:3;
    map1[zx][zy] = 1
    if randint(0, 1) == 1:
        turn = 1
    else:
        turn = 3
    # for(i=0,next=rand()%4;i<4;i++,next=(next+turn)%4)
    next_value = randint(0, 3)
    for i in xrange(0, 4):
        # if(map[zx+2*d[next][0]][zy+2*d[next][1]]==0)
        print "next %d" % next_value, " zx", zx, " zy", zy
        print zx + 2 * d[next_value][0]
        print zy + 2 * d[next_value][1]
        if map1[zx + 2 * d[next_value][0]][zy + 2 * d[next_value][1]] == 0:
            # map[zx+d[next][0]][zy+d[next][1]]=1,
            map1[zx + d[next_value][0]][zy + d[next_value][1]] = 1
            # search(x+d[next][0],y+d[next][1]);
            search(xx + d[next_value][0], yy + d[next_value][1])
        next_value = (next_value + turn) % 4
    # return 0;
    # }
    return 0


# void Make_Maze(int x,int y)
# {
def make_maze(xi, yi):
    # int z1,z2;
    # for(z1=0,z2=2*y+2;z1<=2*x+2;z1++)map[z1][0]=1,map[z1][z2]=1;
    z2 = 2 * yi + 2
    for z1 in xrange(0, 2 * xi + 2 + 1):
        map1[z1][0] = 1
        map1[z1][z2] = 1
    # for(z1=0,z2=2*x+2;z1<=2*y+2;z1++)map[0][z1]=1,map[z2][z1]=1;
    for z1 in xrange(0, 2 * yi + 2 + 1):
        map1[0][z1] = 1
        map1[z2][z1] = 1
    # map[1][2]=1;map[2*x+1][2*y]=1;  srand((unsigned)time(NULL));
    map1[1][2] = 1
    map1[2 * xi + 1][2 * yi] = 1
    # search(rand()%x+1,rand()%y+1);
    search((randint(1, xi)), (randint(1, yi)))
    # }
    return


# int main(void)
# {
def run():
    # int x=8,y=8,z1,z2; //x和y的值指定了这个要生成的迷宫的大小
    x = 8
    y = 8

    # Make_Maze(x,y);
    make_maze(x, y)
    # for(z2=1;z2<=y*2+1;z2++){
    for z2 in xrange(1, y * 2 + 1 + 1):
        # for(z1=1;z1<=x*2+1;z1++) fputs(map[z1][z2]?"　":"█",stdout);
        str = ""
        for z1 in xrange(1, x * 2 + 1 + 1):
            if map1[z1][z2] == 0:
                str += "-" # print "█"
            else:
                str += " " # print " "
        # if(z2<=y*2)putchar(10);
        if z2 <= y * 2:
            print str + "\n"
    # }
    # return 0;
    # }
    return 0


if __name__ == "__main__":
    run()
