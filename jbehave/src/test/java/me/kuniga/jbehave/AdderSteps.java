package me.kuniga.jbehave;

import static org.junit.Assert.*;

import org.jbehave.core.annotations.Aliases;
import org.jbehave.core.annotations.Given;
import org.jbehave.core.annotations.Then;
import org.jbehave.core.annotations.When;

public class AdderSteps {
	
	private Adder adder;
	
	@Given("um somador é criado")
	@Aliases(values={"um somador é instanciado"})
	public void theAdderIsCreated(){
		adder = new Adder();
	}
	
	@When("eu adiciono $a e $b")
	public void iAddTwoNumbers(int a, int b){
		adder.add(a, b);
	}

	@Then("o resultado deve ser $c")
	public void theResultMustBe(int c){
		assertEquals(adder.getResult(), c);
	}

}
