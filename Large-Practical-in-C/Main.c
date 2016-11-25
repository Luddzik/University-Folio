/*
Author: Ludwik Bacmaga
Student Number: s1345559
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INFINITY 2000;
#define NONMEMBER 0;
#define MEMBER 1;

void shPath(int, int, int *);

//global variables
struct MyInput
{
	unsigned int busCapacity;
	unsigned int boardingTime;
	float requestRate;
	float pickupInterval;
	unsigned int maxDelay;
	unsigned int noBuses;
	unsigned int noStops;
	int **map;
	float stopTime;
};

struct MyInput input;

//global variables for time
struct Time
{
	int day;
	int hour;
	int min;
	int sec;
};

struct Time time;

//requests times within hour (based on average request rate)
void requests(int *req)
{
	int temp;
	int r = (input.requestRate + 1);
	int i, j;
	for (i = 0; i < r; i++)
	{
		req[i] = rand() % 60;
	}

	//sort the requests in increasing order
	for (i = 1; i < r; i++) 
	{
		for (j = 0;j<r - i;j++)
		{
			if (req[j] >req[j + 1])
			{
				temp = req[j];
				req[j] = req[j + 1];
				req[j + 1] = temp;
			}
		}
	}
}

//gets source and destination stops for each request
void stops(int *ss, int *ds)
{
	int x = input.requestRate;
	int i;

	//get random variables for each stop and request
	for (i = 0; i <= input.requestRate; i++)
	{
		ss[i] = rand() % x + 1;
		ds[i] = rand() % x + 1;
		while (ss[i] == ds[i]) {
			ss[i] = rand() % x + 1;
			ds[i] = rand() % x + 1;
		}
		//printf("a = %d    b = %d\n", ss[i], ds[i]);
	}
}

//desired pick up time
void pickup(int *picktime)
{
	int p = input.pickupInterval;
	int m = p;
	int s = p;
	int temp = m - s;
	int i;
	//pickup time for each request
	for (i = 0; i <= input.requestRate; i++)
	{
		picktime[i] = rand() % temp + s;
		//printf("%d\n",picktime[i]);
	}
}

void shPath(int s, int t, int *pd) //Dijkstra's Algorithm (Inspired by source code on internet)
{
	int *distance;
	int *perm;
	distance = (int *)malloc(input.noStops*sizeof(int*));
	perm = (int *)malloc(input.noStops*sizeof(int*));

	int current, i, k, dc;
	int smalldist, newdist;
	
	/* initialization of perm and distance array */
	for (i = 0;i<input.noStops;i++)
	{
		perm[i] = NONMEMBER;
		distance[i] = INFINITY;
	}

	perm[s] = MEMBER;
	distance[s] = 0;
	current = s;
	
	//while loop until the current point is not the destination stop
	while (current != t)
	{
		smalldist = INFINITY;
		dc = distance[current];
		for (i = 0; i < input.noStops;i++)
		{
			if (perm[i] == 0)
			{
				if (input.map[current][i] == -1)
				{
					newdist = dc + INFINITY;
					if (newdist < distance[i])
					{
						distance[i] = newdist;
					}
					if (distance[i] < smalldist)
					{
						smalldist = distance[i];
						k = i;
					}
				} 
				else
				{
					newdist = dc + input.map[current][i];
					if (newdist < distance[i])
					{
						distance[i] = newdist;	
					} 
					if (distance[i] < smalldist)
					{
						smalldist = distance[i];
						k = i;
					}
				}
			} /* end of for if */

		}
		current = k;
		perm[current] = MEMBER;
	}  /* END WHILE */
	*pd = distance[t];
	free(distance);
	free(perm);
}

//calculates time and computes which output to print
void costam(int *req, int *ss, int *ds, int *bus, int *picktime)
{

	int pd, sd;

	int reset = 0;
	//requst times, pickup time and random bus stops
	requests(req);
	pickup(picktime);
	stops(ss, ds);

	time.day = 0;
	time.hour = 0;
	time.min = 0;
	time.sec = 0;
	
	int t, i = 0;

	int finish = input.stopTime;
	int finishDay = 0;
	//printf("%d %d", finishDay, finish);
	//incase time is longer than 1 day
	if (finish > 24)
	{
		finishDay = 1;
		finish = finish - 24;
	}

	int *departure, scheduled;
	int distTime;

	int j = 0; //bus counter
	//allocates memory for arrays 
	int *done = (int *)malloc((input.requestRate + 1)*sizeof(int*));

	departure = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	int *departureHour = (int *)malloc((input.requestRate + 1)*sizeof(int*));

	int q;
	for (q = 0; q <= input.requestRate; q++)
	{
		done[q] = 0;
	}

	int *lastStop = (int *)malloc(input.noBuses*sizeof(int*));
	int *freeTime = (int *)malloc(input.noBuses*sizeof(int*));
	int *freeHour = (int *)malloc(input.noBuses*sizeof(int*));
	int *timeSec = (int *)malloc(input.noBuses*sizeof(int*));

	//start at garage (bus stop 0) and time to 0;
	int x;
	for (x = 0; x < input.noBuses; x++)
	{
		lastStop[x] = 0;
		freeTime[x] = 0;
		freeHour[x] = 0;
		timeSec[x] = time.sec;
	}

	int availableTime;

	//argorithm runs as long as the time doesn't equal to finish time.
	while (time.hour != finish)
	{
		if (done[i] == 0)
		{
			if (i == (input.requestRate))
			{
				reset = 1;
			}
			t = req[i];
			time.min = t;
			
			departure[i] = time.min +picktime[i];
			departureHour[i] = time.hour;

			if (departure[i] > 60)
			{
				int temp = departure[i];
				int tempHour = departureHour[i];
				departureHour[i] = tempHour + 1;
				departure[i] = temp - 60;
			}

			shPath(ss[i], ds[i], &pd);
			//printf("stuck here?");
			
			done[i] = 1;
		}
		
		//if the bus is busy, check if it can be free and accept new request
		if (bus[j] == 0)
		{
			int x = departure[i] + input.maxDelay;
			shPath(lastStop[j], ss[i], &sd);
			if ((freeTime[j] + sd) <= x && freeHour[j] <= departureHour[i]) bus[j] = 1;
		}
		//when the bus is free get new request
		if (bus[j] == 1)
		{
			bus[j] = 0;

			shPath(lastStop[j], ss[i], &sd);

			lastStop[j] = ds[i];

			availableTime = freeTime[j] + sd;
			
			int arriveTime, arriveHour;
			//freeHour[j] = time.hour;
			int thour = departureHour[i];
			if (availableTime >= departure[i] && availableTime <= (departure[i] + input.maxDelay))
			{
				if (availableTime > 60)
				{
					thour = thour + 1;
					availableTime = availableTime - 60;
				}
				arriveTime = availableTime;
				int z = availableTime + pd;
				int freeh = thour;
				if (z > 60) 
				{
					freeh = freeh + 1;
					z = z - 60;
				}
				freeHour[j] = freeh;
				freeTime[j] = z;
				arriveHour = thour;
				
			} 
			else
			{
				int z = departure[i] + pd;
				if (z > 60)
				{
					freeHour[j] = departureHour[i] + 1;
					freeTime[j] = z - 60;
				}
				else
				{
					freeHour[j] = departureHour[i];
					freeTime[j] = departure[i] + pd;
				}
				arriveTime = departure[i];
				arriveHour = departureHour[i];
			}

			if (timeSec[j] >= 60)
			{
				timeSec[j] = timeSec[j] - 60;
				time.min = time.min + 1;
				if (time.min > 60)
				{
					time.hour = time.hour + 1;
					time.min = time.min - 60;
				}
				if (time.hour > 24)
				{
					time.hour = time.hour - 24;
					time.day = time.day + 1;
				}
			}

			int zero = 0;
			//print the request message
			printf("%02d:%02d:%02d:%02d -> new request placed from stop %d to stop %d for departure at %02d:%02d:%02d:%02d scheduled for %02d:%02d:%02d:%02d\n", time.day,time.hour,time.min,timeSec[j],ss[i],ds[i],time.day,departureHour[i],departure[i],time.sec,time.day,arriveHour,arriveTime,time.sec);
			//printf("bus: %d free time: %d:%d\n", j, freeHour[j], freeTime[j]);

			j = 0;
			i++;
			//printf("i is: %d", i);
		}  
		else if (j < input.noBuses)
		{
			//printf("i am here\n");
			j++;
		}
		else
		{
			printf("%02d:%02d:%02d:%02d -> new request placed from stop %d to stop %d for departure at %02d:%02d:%02d:%02d cannot be accommodated\n", time.day, time.hour, time.min, time.sec, ss[i], ds[i], time.day, departureHour[i], departure[i], time.sec);
			j = 0;
			i++;
		}

		//one hour has passed, get new random variables
		
		if (reset == 1)
		{
			time.hour = time.hour + 1;
			int z;
			for (z = 0; z <= input.requestRate; z++)
			{
				done[z] = 0;
			}
			i = 0;
			requests(req);
			pickup(picktime);
			stops(ss, ds);
			reset = 0;
		}
	}

	//free the variables names 
	free(done);
	free(lastStop);
	free(freeTime);
	free(freeHour);
	free(timeSec);
	free(departure);
	free(departureHour);
	//printf("left loooop");
}

//main function 
void main(int argc, char *argv[])
{
	char c[100];
	FILE *file;
	int k = 0;

	if ((file = fopen(argv[1], "r+")) == NULL) {
		printf("Error! opening file");
		exit(1); // Program exits if file pointer returns NULL. /
	}

	while (fgets(c, sizeof(c), file) != NULL) {
		char *bc = "busCapacity";
		char *bt = "boardingTime";
		char *rt = "requestRate";
		char *pi = "pickupInterval";
		char *md = "maxDelay";
		char *nb = "noBuses";
		char *ns = "noStops";
		char *m = "map";
		char *st = "stopTime";

		if (c[0] == '#') {}
		else
		{
			if (strstr(c, bc))
			{
				sscanf(c, "busCapacity %d", &input.busCapacity); //puts the input from file to the variable.
																 //printf("Bus Capacity is: %d\n", input.busCapacity); //checks if the correct input is in the file.
			}
			else if (strstr(c, bt))
			{
				sscanf(c, "boardingTime %d", &input.boardingTime); //puts the input from file to the variable.
																   //printf("Boarding Time is: %d\n", input.boardingTime); //checks if the correct input is in the file.
			}
			else if (strstr(c, rt))
			{
				sscanf(c, "requestRate %f", &input.requestRate); //puts the input from file to the variable.
																 //printf("Request Rate is: %.1f\n", input.requestRate); //checks if the correct input is in the file.
			}
			else if (strstr(c, pi))
			{
				sscanf(c, "pickupInterval %f", &input.pickupInterval); //puts the input from file to the variable.
																	   //printf("Pickup Interval is: %.1f\n", input.pickupInterval); //checks if the correct input is in the file.
			}
			else if (strstr(c, md))
			{
				sscanf(c, "maxDelay %d", &input.maxDelay); //puts the input from file to the variable.
														   //printf("Max Delay is: %d\n", input.maxDelay); //checks if the correct input is in the file.
			}
			else if (strstr(c, nb))
			{
				sscanf(c, "noBuses %d", &input.noBuses); //puts the input from file to the variable.
														 //printf("Number of Buses is: %d\n", input.noBuses); //checks if the correct input is in the file.
			}
			else if (strstr(c, ns))
			{
				sscanf(c, "noStops %d", &input.noStops); //puts the input from file to the variable.
														 //printf("Number of Stops is: %d\n", input.noStops); //checks if the correct input is in the file.

														 //initialise double array
				int i, n = input.noStops;

				//printf("%d", n);
				//need to initialise N to be size of array (rows in the input, count).
				input.map = (int **)malloc(n*sizeof(int*)); // rows

				for (i = 0; i < n; i++)
				{
					input.map[i] = (int *)malloc(n*sizeof(int)); // columns
				}
			}
			else if (strstr(c, m) || (!strstr(c, st) && !strstr(c, ns) && !strstr(c, nb) && !strstr(c, md) && !strstr(c, pi) && !strstr(c, rt) && !strstr(c, bt) && !strstr(c, bc)))
			{
				//map needs to be after noStops variable.
				int j, N = input.noStops;

				if (!strstr(c, m))
				{
					char **res = NULL;
					char *p = strtok(c, " ");
					int n_spaces = 0, i;
					/* split string and append tokens to 'res' */

					while (p) {
						res = realloc(res, sizeof(char*) * ++n_spaces);

						if (res == NULL)
							exit(-1); /* memory allocation failed */

						res[n_spaces - 1] = p;

						p = strtok(NULL, " ");
					}

					/* realloc one extra element for the last NULL */

					res = realloc(res, sizeof(char*) * (n_spaces + 1));
					res[n_spaces] = 0;


					for (j = 0; j < N; j++)
					{
						sscanf(res[j], "%d", &input.map[k][j]);

					}
					//printf(input.map[k][j]);
					k = k + 1;
					free(res);
				}
			}
			else if (strstr(c, st))
			{
				sscanf(c, "stopTime %f", &input.stopTime); //puts the input from file to the variable.
														   //printf("Stop Time is: %.0f\n", input.stopTime); //checks if the correct input is in the file.
			}
			else
			{
				printf("Error! Wrong variable name");
				exit(1); // Program exits if file pointer returns NULL. /
			}
			//printf(c);
		}

	}

	//allocate array space for all the requests, stops, pickup time
	int *req;
	int *ss, *ds;
	int *bus;
	int *picktime;
	req = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	ss = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	ds = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	picktime = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	bus = (int *)malloc(input.noBuses*sizeof(int*));

	//sets buses to be free
	int i;
	for (i = 0; i < input.noBuses; i++)
	{
		bus[i] = 1;
	}

	costam(req, ss, ds, bus, picktime);

	//to deallocate memory, do this:
	int N = input.noStops;
	for (i = 0; i < N; i++)
	{
		free(input.map[i]);
	}
	//free all memory
	free(input.map);
	free(picktime);
	free(req);
	free(ss);
	free(ds);
	free(bus);
	fclose(file);
}

/*void costam(int *req, int *ss, int *ds, int *bus, int *picktime)
{

	int pd, sd;

	int reset = 0;

	requests(req);
	pickup(picktime);
	stops(ss, ds);

	time.day = 0;
	time.hour = 0;
	time.min = 0;
	time.sec = 0;
	
	int t, i = 0;

	int finish = input.stopTime;
	int finishDay = 0;
	//printf("%d %d", finishDay, finish);
	//incase time is longer than 1 day
	if (finish > 24)
	{
		finishDay = 1;
		finish = finish - 24;
	}

	int *departure, scheduled;
	int distTime;

	int j = 0; //bus counter

	int *done = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	int *firstBusLeave = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*)); //stored first bus that will leave stop
	int *busLeaveH = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*));
	int *busLeaveD = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*));
	int *nobus = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*)); //which bus will leave first
	int *inOut = (int *)malloc(2*(input.requestRate + 1)*input.stopTime*sizeof(int*));
	int *firstBusArrive = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*)); //stored first bus that will arrive at stop
	int *busArriveH = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*));
	int *busArriveD = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*));
	int *busStopNo = (int *)malloc(2 * (input.requestRate + 1)*input.stopTime*sizeof(int*));
	int *arriveBus = (int *)malloc(2*(input.requestRate + 1)*input.stopTime*sizeof(int*)); //which bus will arrive first
	int *lastBusStop = (int *)malloc(2*(input.requestRate + 1)*input.stopTime*sizeof(int*));
	departure = (int *)malloc((input.requestRate + 1)*sizeof(int*));
	int *departureHour = (int *)malloc((input.requestRate + 1)*sizeof(int*));

	int q;
	for (q = 0; q <= input.requestRate; q++)
	{
		done[q] = 0;
		firstBusArrive[q] = INFINITY;
		busArriveD[q] = INFINITY;
		busArriveH[q] = INFINITY;
		firstBusLeave[q] = INFINITY;
		busLeaveD[q] = INFINITY;
		busLeaveH[q] = INFINITY;
		inOut[q] = 0;
		nobus[q] = 0;
		arriveBus[q] = 0;
		busStopNo[q] = 0;
		lastBusStop[q] = 0;
	}

	int *capacity = (int *)malloc(input.noBuses*sizeof(int*));
	int *lastStop = (int *)malloc(input.noBuses*sizeof(int*));
	int *arriveStop = (int *)malloc(input.noBuses*sizeof(int*));
	int *freeTime = (int *)malloc(input.noBuses*sizeof(int*));
	int *freeHour = (int *)malloc(input.noBuses*sizeof(int*));
	int *timeSec = (int *)malloc(input.noBuses*sizeof(int*));
	int *busleaveTime = (int *)malloc(input.noBuses*sizeof(int*));
	int *busleaveHour = (int *)malloc(input.noBuses*sizeof(int*));
	int *busleaveDay = (int *)malloc(input.noBuses*sizeof(int*));
	int *busarriveTime = (int *)malloc(input.noBuses*sizeof(int*));
	int *busarriveHour = (int *)malloc(input.noBuses*sizeof(int*));
	int *busarriveDay = (int *)malloc(input.noBuses*sizeof(int*));

	//start at garage (bus stop 0) and time to 0;
	int x;
	for (x = 0; x < input.noBuses; x++)
	{
		lastStop[x] = 0;
		arriveStop[x] = 0;
		freeTime[x] = 0;
		capacity[x] = 0;
		freeHour[x] = 0;
		timeSec[x] = time.sec;
		busleaveTime[x] = INFINITY;
		busleaveHour[x] = INFINITY;
		busleaveDay[x] = INFINITY;
		busarriveTime[x] = INFINITY;
		busarriveHour[x] = INFINITY;
		busarriveDay[x] = INFINITY;
	}

	int availableTime;

	int nr = 0; //new request
	int ls = 0; //bus leave stop
	int as = 0; //bus arrive stop

	int k = 0, c1 = 0, c2 = 0, bs = 0, ba = 0, in = 0;

	int requestHour = 0;

	while (time.hour != finish)
	{
		
		//printf("%d\n", firstBusLeave[c2]);
		if (req[i] < firstBusLeave[c1] && requestHour <= busLeaveH[c1] && req[i] < firstBusArrive[c2] && requestHour <= busArriveH[c2])
		{
			if (done[i] == 0)
			{
				nr = 1;
				if (i == (input.requestRate))
				{
					reset = 1;
				}
				t = req[i];
				time.min = t;
				
				departure[i] = time.min +picktime[i];
				departureHour[i] = time.hour;

				if (departure[i] > 60)
				{
					int temp = departure[i];
					int tempHour = departureHour[i];
					departureHour[i] = tempHour + 1;
					departure[i] = temp - 60;
				}

				shPath(ss[i], ds[i], &pd);
				//printf("stuck here?");
				
				done[i] = 1;
			}
		}
		else if (req[i] == firstBusLeave[c1] && requestHour <= busLeaveH[c1] && req[i] < firstBusArrive[c2] && requestHour <= busArriveH[c2])
		{
			if (done[i] == 0)
			{
				nr = 1;
				if (i == (input.requestRate))
				{
					reset = 1;
				}
				t = req[i];
				time.min = t;

				departure[i] = time.min + picktime[i];
				departureHour[i] = time.hour;

				if (departure[i] > 60)
				{
					int temp = departure[i];
					int tempHour = departureHour[i];
					departureHour[i] = tempHour + 1;
					departure[i] = temp - 60;
				}

				shPath(ss[i], ds[i], &pd);
				//printf("stuck here?");
				done[i] = 1;
			}
			ls = 1;
		}
		else if (req[i] < firstBusLeave[c1] && requestHour <= busLeaveH[c1] && req[i] == firstBusArrive[c2] && requestHour <= busArriveH[c2])
		{
			if (done[i] == 0)
			{
				nr = 1;
				if (i == (input.requestRate))
				{
					reset = 1;
				}
				t = req[i];
				time.min = t;

				departure[i] = time.min  + picktime[i];
				departureHour[i] = time.hour;

				if (departure[i] > 60)
				{
					int temp = departure[i];
					int tempHour = departureHour[i];
					departureHour[i] = tempHour + 1;
					departure[i] = temp - 60;
				}

				shPath(ss[i], ds[i], &pd);
				//printf("stuck here?");
				done[i] = 1;
			}
			as = 1;
		}
		else if (req[i] == firstBusLeave[c1] && requestHour <= busLeaveH[c1] && req[i] == firstBusArrive[c2] && requestHour <= busArriveH[c2])
		{
			if (done[i] == 0)
			{
				nr = 1;
				if (i == (input.requestRate))
				{
					reset = 1;
				}
				t = req[i];
				time.min = t;

				departure[i] = time.min + picktime[i];
				departureHour[i] = time.hour;

				if (departure[i] > 60)
				{
					int temp = departure[i];
					int tempHour = departureHour[i];
					departureHour[i] = tempHour + 1;
					departure[i] = temp - 60;
				}

				shPath(ss[i], ds[i], &pd);
				//printf("stuck here?");
				done[i] = 1;
			}
			ls = 1;
			as = 1;
		}
		else if (firstBusLeave[c1] < firstBusArrive[c2])
		{
			ls = 1;
		} 
		else if (firstBusLeave[c1] == firstBusArrive[c2])
		{
			as = 1;
			ls = 1;
		}
		else //bus arrives first
		{
			as = 1;
		} 
		
		//leave and arrive stop order
		
		
		if (bus[j] == 0)
		{
			int x = departure[i] + input.maxDelay;
			shPath(lastStop[j], ss[i], &sd);
			if ((freeTime[j] + sd) <= x && freeHour[j] <= departureHour[i]) bus[j] = 1;
		}

		if (bus[j] == 1 && nr == 1)
		{
			nr = 0;
			bus[j] = 0;

			shPath(lastStop[j], ss[i], &sd);
			
			lastBusStop[bs] = lastStop[j];
			bs++;
			
			arriveStop[j] = ss[i];

			lastBusStop[bs] = arriveStop[j];
			bs++;

			busStopNo[ba] = arriveStop[j];
			ba++;

			lastStop[j] = ds[i];

			busStopNo[ba] = lastStop[j];
			ba++;

			distTime = pd + sd; //sum distance from two points and from the bus stop position
			availableTime = freeTime[j] + sd;
			
			int arriveTime, arriveHour;
			//freeHour[j] = time.hour;
			int thour = departureHour[i];
			if (availableTime >= departure[i] && availableTime <= (departure[i] + input.maxDelay))
			{
				if (availableTime > 60)
				{
					thour = thour + 1;
					availableTime = availableTime - 60;
				}
				arriveTime = availableTime;
				int z = availableTime + pd;
				int freeh = thour;
				if (z > 60) 
				{
					freeh = freeh + 1;
					z = z - 60;
				}
				freeHour[j] = freeh;
				freeTime[j] = z;
				arriveHour = thour;
				
			} 
			else
			{
				int z = departure[i] + pd;
				if (z > 60)
				{
					freeHour[j] = departureHour[i] + 1;
					freeTime[j] = z - 60;
				}
				else
				{
					freeHour[j] = departureHour[i];
					freeTime[j] = departure[i] + pd;
				}
				arriveTime = departure[i];
				arriveHour = departureHour[i];
			}
			
			//for bus leaving stop;
			busleaveDay[j] = time.day;
			busleaveHour[j] = arriveHour;
			busleaveTime[j] = arriveTime - sd;
			
			if (busleaveTime[j] < 0)
			{
				int temp = 60;
				busleaveTime[j] = temp + (arriveTime - sd);
				busleaveHour[j] = busleaveHour[j] - 1;
				if (busleaveHour[j] < 0)
				{
					busleaveHour[j] = 24;
					busleaveDay[j] = busleaveDay[j] - 1;
				}
			}

			//for bus arriving stop
			busarriveDay[j] = time.day;
			busarriveHour[j] = arriveHour;
			busarriveTime[j] = arriveTime;

			if (timeSec[j] >= 60)
			{
				timeSec[j] = timeSec[j] - 60;
				time.min = time.min + 1;
				if (time.min > 60)
				{
					time.hour = time.hour + 1;
					time.min = time.min - 60;
				}
				if (time.hour > 24)
				{
					time.hour = time.hour - 24;
					time.day = time.day + 1;
				}
			}

			int zero = 0;

			inOut[in] = 1;
			in++;
			inOut[in] = 0;
			in++;

			printf("%02d:%02d:%02d:%02d -> new request placed from stop %d to stop %d for departure at %02d:%02d:%02d:%02d scheduled for %02d:%02d:%02d:%02d\n", time.day,time.hour,time.min,timeSec[arriveBus[c2]],ss[i],ds[i],time.day,departureHour[i],departure[i],time.sec,time.day,arriveHour,arriveTime,time.sec);
			//printf("bus: %d free time: %d:%d\n", j, freeHour[j], freeTime[j]);

			busLeaveD[k] = busleaveDay[j];
			busLeaveH[k] = busleaveHour[j];
			firstBusLeave[k] = busleaveTime[j];
			nobus[k] = j;

			busArriveD[k] = busarriveDay[j];
			busArriveH[k] = busarriveHour[j];
			firstBusArrive[k] = busarriveTime[j];
			arriveBus[k] = j;

			k++;

			busLeaveD[k] = busarriveDay[j];
			busLeaveH[k] = busarriveHour[j];
			firstBusLeave[k] = busarriveTime[j];
			nobus[k] = j;
			
			busArriveD[k] = busarriveDay[j];
			busArriveH[k] = freeHour[j];
			firstBusArrive[k] = freeTime[j];
			arriveBus[k] = j;

			k++;

			j = 0;
			i++;
			//printf("i is: %d", i);
		}  
		else if (j < input.noBuses)
		{
			//printf("i am here\n");
			j++;
		}
		else
		{
			printf("%02d:%02d:%02d:%02d -> new request placed from stop %d to stop %d for departure at %02d:%02d:%02d:%02d cannot be accommodated\n", time.day, time.hour, time.min, timeSec[arriveBus[c2]], ss[i], ds[i], time.day, departureHour[i], departure[i], time.sec);
			j = 0;
			i++;
		}

		//printf("%d\n", firstBusLeave[1]);
		if (as == 1)
		{
			as = 0;
			time.min = firstBusArrive[c2];
			time.day = busArriveD[c2];
			time.hour = busArriveH[c2];

			printf("%02d:%02d:%02d:%02d -> minibus %d arrived at stop %d\n", time.day, time.hour, time.min, timeSec[arriveBus[c2]], arriveBus[c2], busStopNo[c2]);
			timeSec[arriveBus[c2]] = timeSec[arriveBus[c2]] + 10;
			if (timeSec[arriveBus[c2]] >= 60)
			{
				timeSec[arriveBus[c2]] = timeSec[arriveBus[c2]] - 60;
				time.min = time.min + 1;
				if (time.min > 60)
				{
					time.hour = time.hour + 1;
					time.min = time.min - 60;
				}
				if (time.hour > 24)
				{
					time.hour = time.hour - 24;
					time.day = time.day + 1;
				}
			}
			if (inOut[c2] == 1)
			{
				printf("%02d:%02d:%02d:%02d -> minibus %d boarded passenger at stop %d\n", time.day, time.hour, time.min, timeSec[arriveBus[c2]], arriveBus[c2], busStopNo[c2]);
				capacity[arriveBus[c2]] = capacity[arriveBus[c2]] + 1;
				if (capacity[arriveBus[c2]] >= input.busCapacity)
				{
					printf("Minibus %d is full!", arriveBus);
				}
				else
				{
					printf("%02d:%02d:%02d:%02d -> minibus %d occupancy became %d\n", time.day, time.hour, time.min, timeSec[arriveBus[c2]], arriveBus[c2], capacity[arriveBus[c2]]);
				}
			}
			else
			{
				printf("%02d:%02d:%02d:%02d -> minibus %d disembarked passenger at stop %d\n", time.day, time.hour, time.min, timeSec[arriveBus[c2]], arriveBus[c2], busStopNo[c2]);
				capacity[arriveBus[c2]] = capacity[arriveBus[c2]] - 1;
				if (capacity[arriveBus[c2]] < 0)
				{
					printf("Minibus %d can't have less than 0 people\n", arriveBus[c2]);
				}
				else
				{
					printf("%02d:%02d:%02d:%02d -> minibus %d occupancy became %d\n", time.day, time.hour, time.min, timeSec[arriveBus[c2]], arriveBus[c2], capacity[arriveBus[c2]]);
				}
			}

			c2++;
		}

		if (ls == 1)
		{
			ls = 0;
			time.day = busLeaveD[c1];
			time.hour = busLeaveH[c1];
			if (time.min == (firstBusLeave[c1] + 1))
			{
				time.min = firstBusLeave[c1] + 1;
			}
			else
			{
				time.min = firstBusLeave[c1];
			}

			printf("%02d:%02d:%02d:%02d -> minibus %d left stop %d\n", time.day, time.hour, time.min, timeSec[nobus[c1]], nobus[c1], lastBusStop[c1]);
			c1++;
		}

		//one hour has passed, get new random variables
		
		if (reset == 1)
		{
			time.hour = time.hour + 1;
			int z;
			for (z = 0; z <= input.requestRate; z++)
			{
				done[z] = 0;
			}
			i = 0;
			requestHour = requestHour + 1;
			requests(req);
			pickup(picktime);
			stops(ss, ds);
			reset = 0;
		}
	}
	
}*/
