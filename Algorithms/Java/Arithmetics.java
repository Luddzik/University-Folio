package imult;

import java.io.File;

public class Arithmetics {
  public static BigInt add(BigInt A, BigInt B) {
	  DigitCarry dc = new DigitCarry(); //create variable which will store digit and carry from arithmetic.
	  
	  BigInt sum = new BigInt();  //create variable of class BigInt to give back the result (result variable)
	  
	  for (int i = 0; i<= Math.max(A.length(), B.length()); i++){   //loop which adds A[i] + B[i] +carry and puts it in the result variable.
		  dc = Arithmetic.addDigits(A.getDigit(i), B.getDigit(i), dc.carry()); //digit and carry are stored in dc variable.
		  sum.setDigit(i, dc.digit()); //saves the result to the sum
	  }
	  return sum;  
  }
  
  public static BigInt sub(BigInt A, BigInt B) {
      DigitCarry dc = new DigitCarry(); //create variable which will store digit and carry from arithmetic.
	  
	  BigInt sub = new BigInt();   //create variable of class BigInt to give back the result (result variable)
	  
	  for (int i = 0; i<= Math.max(A.length(), B.length()); i++){   //loop which subtracts B[i] +carry from A[i] (if A[i]>=(B[i]+carry) and puts the answer in the results variable.
		  dc = Arithmetic.subDigits(A.getDigit(i), B.getDigit(i), dc.carry()); //digit and carry are stored in dc variable.
		  sub.setDigit(i, dc.digit()); //result is being stored in the result variable (sub)
	  }
	  return sub; 
  }
  
  public static BigInt koMul(BigInt A, BigInt B) {
	  int n = Math.max(A.length(), B.length()); //gets the maximum length between A and B and stores it in n.

	  if (n <= 1) { //if the length is '<=1' than multiply both inputs and return the result.
		  DigitCarry dc = Arithmetic.mulDigits(A.getDigit(0), B.getDigit(0)); //multiply the digits and store the result in variable dc.
		  BigInt result = new BigInt(2); //create variable result of length 2 for storing digit and carry.
		  result.setDigit(0, dc.digit()); //save digit as first element
		  result.setDigit(1, dc.carry()); //save carry as second element
		  return result; 
	  }
	  	
	  int floor = n/2 -1; //calculates the floor
	  int ceiling = floor +1; //calculates the ceiling
	  
	  //splits the input A into a0 and a1, of length depending on the length of the max input
	  BigInt a0 = A.split(0, floor); 
	  BigInt a1 = A.split(ceiling, n-1);

	  //splits the input B into b0 and b1, of length depending on the length of the max input
	  BigInt b0 = B.split(0, floor);
	  BigInt b1 = B.split(ceiling, n-1);

	  //calculates variable 'l' (using variables a0, a1) and 'h' (using variables b0, b1) recursively 
	  BigInt l = koMul(a0, b0);
	  BigInt h = koMul(a1, b1);
	
	  //calculates 'a' and 'b' by the formula a=a0+a1 (same for 'b'), needed to calculate m
	  BigInt a = add(a0, a1);
	  BigInt b = add(b0, b1);
	  BigInt haddl = add(h, l); //adds the 'h' and 'l' result, which than will be subtracted from a*b
	  BigInt m = sub(koMul(a, b), haddl); //calculates the m variable by the formula 'm=(a0+a1)(b0+b1)-l-h'
	
	  //m variable needs to be multiplied by base to power ceiling for final result
	  m.lshift(ceiling);
	  h.lshift(2*(ceiling)); //h variable is multiplied by base to power 2*ceiling

	  //creates result variable which calculates the result using formula 'l+(m*B^floor)+(h*B^2*floor)'
	  BigInt result = add(l, (add(m, h)));
	
	  return result;
  }
  
  public static BigInt koMulOpt(BigInt A, BigInt B) {
	  int n = Math.max(A.length(), B.length()); //gets the maximum length between A and B and stores it in n.
	  	
	  if (n <= 10) { //if the length of n is not bigger than 10 than schoolMul arithmetic is performed
		  BigInt result = Arithmetic.schoolMul(A, B);
		  return result;
	  }
	  else { //if length of input is greater than 10 than same code as koMul is performed.
		  if (n <= 1) { //if the length is '<=1' than multiply both inputs and return the result.
			  DigitCarry dc = Arithmetic.mulDigits(A.getDigit(0), B.getDigit(0)); //multiply the digits and store the result in variable dc.
			  BigInt result = new BigInt(2); //create variable result of length 2 for storing digit and carry.
			  result.setDigit(0, dc.digit()); //save digit as first element
			  result.setDigit(1, dc.carry()); //save carry as second element
			  return result; 
		  }
		  	
		  int floor = n/2 -1; //calculates the floor
		  int ceiling = floor +1; //calculates the ceiling
		  
		  //splits the input A into a0 and a1, of length depending on the length of the max input
		  BigInt a0 = A.split(0, floor); 
		  BigInt a1 = A.split(ceiling, n-1);

		  //splits the input B into b0 and b1, of length depending on the length of the max input
		  BigInt b0 = B.split(0, floor);
		  BigInt b1 = B.split(ceiling, n-1);

		  //calculates variable 'l' (using variables a0, a1) and 'h' (using variables b0, b1) recursively 
		  BigInt l = koMul(a0, b0);
		  BigInt h = koMul(a1, b1);
		
		  //calculates 'a' and 'b' by the formula a=a0+a1 (same for 'b'), needed to calculate m
		  BigInt a = add(a0, a1);
		  BigInt b = add(b0, b1);
		  BigInt haddl = add(h, l); //adds the 'h' and 'l' result, which than will be subtracted from a*b
		  BigInt m = sub(koMul(a, b), haddl); //calculates the m variable by the formula 'm=(a0+a1)(b0+b1)-l-h'
		
		  //m variable needs to be multiplied by base to power ceiling for final result
		  m.lshift(ceiling);
		  h.lshift(2*(ceiling)); //h variable is multiplied by base to power 2*ceiling

		  //creates result variable which calculates the result using formula 'l+(m*B^floor)+(h*B^2*floor)'
		  BigInt result = add(l, (add(m, h)));
		
		  return result;
	  }
  }
  
  public static void main(String argv[]) {

  }
}
