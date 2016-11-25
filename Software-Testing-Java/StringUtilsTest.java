package Code;

import static org.junit.Assert.*;

import java.io.IOException;
import java.util.InputMismatchException;

import org.junit.Test;
import org.junit.rules.ExpectedException;

public class StringUtilsTest {

	
	
	
	//ERROR TESTS
	
	
	@Test
	public void inputTextNullError() {
		assertNull((StringUtils.replaceString(null, "this", "THAT", '#', true)));
	}
	
	
	//Null delimiter in combination with active inside flag causes undefined behaviour.
	@Test
	public void delimiterNullError() {
		try{
			assertTrue((StringUtils.replaceString("#this#", "this", "THAT", null, true).equals("#this#")));
		}
		catch(RuntimeException e){
		}
	}
	
	//SINGLE TESTS
	
	@Test
	public void inputTextEmptyTest() {
		assertTrue((StringUtils.replaceString("", "bad", "l", '#', true).equals("")));
	}
	
	@Test
	public void inputLTpatternLengthTest() {
		assertTrue((StringUtils.replaceString("Clock", "Clocked", "CLOCKED", '#', false).equals("Clock")));
	}
	
	@Test
	public void inputEQpatternLengthTest() {
		assertTrue((StringUtils.replaceString("bad", "bad", "l", '#', false).equals("l")));
	}
	
	@Test
	public void patternNullTest() {
		assertTrue((StringUtils.replaceString("Clock", null, "l", '#', true).equals("Clock")));
	}
	
	@Test
	public void patternEmptyTest() {
		assertTrue((StringUtils.replaceString("Clock", "", "l", '#', true).equals("Clock")));
	}
	
	@Test
	public void patternSingleCharacterTest() {
		assertTrue((StringUtils.replaceString("Clock", "b", "l", '#', true).equals("Clock")));
	}
	
	@Test
	public void replacementNullTest() {
		assertTrue((StringUtils.replaceString("Clock # house # dog", "dog", null, '#', false).equals("Clock # house # ")));
	}
	
	@Test
	public void replacementEmptyTest() {
		assertTrue((StringUtils.replaceString("Clock # house # dog", "dog", "", '#', false).equals("Clock # house # ")));
	}
	
	@Test
	public void replacementSingleCharacter() {
		assertTrue((StringUtils.replaceString("Clock # house # dog", "dog", "?", '#', false).equals("Clock # house # ?")));
	}
	
	@Test
	public void containsOneDelimiterTest() {
		assertTrue((StringUtils.replaceString("Change this # not this and this", "dis", "THAT", '#', true).equals("Change this # not this and this")));
	}
	
	@Test
	public void delimiterNullError2() {
		assertTrue((StringUtils.replaceString("#this#", "this", "THAT", null, false).equals("#THAT#")));
	}
	
	@Test
	public void inputGTpattern_NoDelim_NoPattern_insideTrueTest() {
		assertTrue((StringUtils.replaceString("Change this not this and this", "dis", "THAT", '#', true).equals("Change this not this and this")));
	}
	
	@Test
	public void inputGTpattern_NoDelim_NoPattern_insideFalseTest() {
		assertTrue((StringUtils.replaceString("Change this not this and this", "dis", "THAT", '#', false).equals("Change this not this and this")));
	}
	
	@Test
	public void inputGTpattern_MultipleDelim_NoPattern_insideTrueTest() {
		assertTrue((StringUtils.replaceString("Change # this # not this # and this #", "dis", "THAT", '#', true).equals("Change # this # not this # and this #")));
	}
	
	
	@Test
	public void inputGTpattern_MultipleDelim_NoPattern_insideFalseTest() {
		assertTrue((StringUtils.replaceString("Change # this # this # and this #", "dis", "THAT", '#', false).equals("Change # this # this # and this #")));
	}
	
	@Test
	public void inputGTpattern_MultipleDelim_PatternOnlyInAR_insideTrueTest() {
		assertTrue((StringUtils.replaceString("Change # this # not dis # and this #", "this", "THAT", '#', true).equals("Change # THAT # not dis # and THAT #")));
	}
	
	@Test
	public void inputGTpattern_MultipleDelim_PatternOnlyInAR_insideFalseTest() {
		assertTrue((StringUtils.replaceString("Change # this # not dis # and this #", "this", "THAT", '#', false).equals("Change # this # not dis # and this #")));
	}

	@Test
	public void inputGTpattern_MultipleDelim_PatternOnlyOutsideAR_insideTrueTest() {
		assertTrue((StringUtils.replaceString("Change # dis # not this # and dis #", "this", "THAT", '#', true).equals("Change # dis # not this # and dis #")));
	}
	
	@Test
	public void inputGTpattern_MultipleDelim_PatternOnlyOutsideAR_insideFalseTest() {
		assertTrue((StringUtils.replaceString("Change # not dis # this # and not dis #", "this", "THAT", '#', false).equals("Change # not dis # THAT # and not dis #")));
	}

	@Test
	public void inputGTpattern_MultipleDelim_PatternInAndOutsideAR_insideTrueTest() {
		assertTrue((StringUtils.replaceString("Change # this # not this # and this #", "this", "THAT", '#', true).equals("Change # THAT # not this # and THAT #")));
	}
	
	@Test
	public void inputGTpattern_MultipleDelim_PatternInAndOutsideAR_insideFalseTest() {
		assertTrue((StringUtils.replaceString("Change # not this # this # and not this #", "this", "THAT", '#', false).equals("Change # not this # THAT # and not this #")));
	}
	
	
	
}
