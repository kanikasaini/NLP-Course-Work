def editdistance(first, second):
	if (len(first) < len(second)):
		temp = first;
		first = second;
		second = temp;

	m = len(first);
	n = len(second);
	dp = [ [0 for i in range(n+1)] for j in range(m+1) ];
	for i in range(m+1):
		for j in range(n+1):
			if (i==0):
				dp[i][j] = j;
			elif (j==0):
				dp[i][j] = i;
			elif (first[i-1]==second[j-1]):
				dp[i][j] = dp[i-1][j-1];
			else:
				dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1] + 1);

	print("Minimum edit distance: " + str(dp[m][n]) + "\n");

	op = "";
	output = "";
	i = m;
	j = n;
	cnt = 0;
	while (i>0 or j>0):
		if (i >0 and j>0 and first[i-1] == second[j-1]):
			op = "n" + op;
			output = first[i-1] + output;
			cnt -=1;
			i-=1;
			j-=1;
		elif (i>0 and j>0 and dp[i][j] == dp[i-1][j-1] + 2):
			output = second[j-1] + output;
			op = 's' + op;
			cnt-=1;
			i-=1;
			j-=1;
		elif (i>0 and dp[i][j] == dp[i-1][j] + 1):
			output = '*' + output;
			op = 'd' + op;
			cnt-=1;
			i-=1;
		elif (j>0 and dp[i][j] == dp[i][j-1] + 1):
			output = second[j-1] + output;
			op = 'i' + op;
			cnt-=1;
			j-=1;

	print(first);
	print(str(output) + "\n" + str(op));

	return;

first = input("Enter first string: ");
second = input("Enter second string: ");
editdistance(first, second);
