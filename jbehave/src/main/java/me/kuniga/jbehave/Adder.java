package me.kuniga.jbehave;

public class Adder {

	private int result;
	
	public void add(int a, int b){
		result = a + b;
	}
	
	public int getResult(){
		return result;
	}
	
}
