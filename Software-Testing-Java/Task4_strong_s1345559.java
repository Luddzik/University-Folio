/*
 * Author: Ludwik Bacmaga
 * Student number: s1345559
 */
package Code;

import static org.junit.Assert.*;

import java.io.IOException;
import java.util.InputMismatchException;

import org.junit.Test;
import org.junit.rules.ExpectedException;

public class Task4_strong_s1345559 {
	
	@Test
	public void outside_atomic_region(){
		assertFalse(StringUtils2.replaceString("1 # 12 # 123 # 1234 # 12345", "1", "boom", '#', false).equals(StringUtils.replaceString("1 # 12 # 123 # 1234 # 12345", "1", "boom", '#', false)));
	}
	
	@Test
	public void inside_atomic_region(){
		assertFalse(StringUtils2.replaceString("1 # 12 # 123 # 1234 # 12345", "1", "boom", '#', true).equals(StringUtils.replaceString("1 # 12 # 123 # 1234 # 12345", "1", "boom", '#', true)));
	}
	
	@Test
	public void middle_pattern_outside(){
		assertFalse(StringUtils2.replaceString("1 # 12 # 123 # 1234 # 12345", "12", "boom", '#', false).equals(StringUtils.replaceString("1 # 12 # 123 # 1234 # 12345", "12", "boom", '#', false)));
	}
	
	@Test
	public void middle_pattern_inside(){
		assertFalse(StringUtils2.replaceString("1 # 12 # 123 # 1234 # 12345", "12", "boom", '#', true).equals(StringUtils.replaceString("1 # 12 # 123 # 1234 # 12345", "12", "boom", '#', true)));
	}
	
	@Test
	public void multiple_pattern_inside(){
		assertFalse(StringUtils2.replaceString("1 # 1212 # 123 # 12341234 # 12345 #", "12", "boom", '#', true).equals(StringUtils.replaceString("1 # 1212 # 123 # 12341234 # 12345 #", "12", "boom", '#', true)));
	}
	
	@Test
	public void multiple_pattern_outside(){
		assertFalse(StringUtils2.replaceString("1 # 1212 # 123123 # 12341234 # 12345 #", "12", "boom", '#', false).equals(StringUtils.replaceString("1 # 1212 # 123123 # 12341234 # 12345 #", "12", "boom", '#', false)));
	}
	
	@Test
	public void composite_test(){
		assertTrue(StringUtils2.replaceString("out # in # out", "inout", "check", '#', true).equals("out # in # out"));
	}
	
	@Test
	public void last_segment_change(){
		assertTrue(StringUtils2.replaceString("hi# in # som txt", "txt", "out", '#', false).equals("hi# in # som out"));
	}
	
	@Test
	public void no_patterns(){
		assertTrue(StringUtils2.replaceString("hi# in # som txt", "ini", "out", '#', false).equals("hi# in # som txt"));
	}
}
