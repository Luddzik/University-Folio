/**
 * File:   MH_Lexer.java
 * Date:   October 2014
 *
 * Java template file for lexer component of Informatics 2A Assignment 1 (2014).
 * Concerns lexical classes and lexer for the language MH (`Micro-Haskell').
 */

import java.io.* ;

class VarAcceptor extends GenAcceptor {

    public String lexClass() {
        return "VAR";
    }
    public int totalStates() {
        return 4;
    }
    public int nextState (char c, int state) {
        switch (state) {
            case 0:  if(Character.isLowerCase(c)){
            	return 1;
            } else{
            	return 3;
            }
            case 1: if(Character.isLowerCase(c) || Character.isUpperCase(c) || Character.isDigit(c)){
            	return 1;
            } else if(c=='\''){
            	return 2;
            }else{
            	return 3;
            }
            case 2: if(c=='\''){
            	return 2;
            } else{
            	return 3;
            }
            default: return 3; // garbage state, declared "dead" below
        }
    }
    public boolean isGoalState(int state) {
        return (state == 1 || state == 2);
    }
    public boolean isDeadState(int state) {
        return (state == 3);
    }
	
}

class NumAcceptor extends GenAcceptor {

    public String lexClass() {
        return "NUM";
    }
    public int totalStates() {
        return 3;
    }
    public int nextState (char c, int state) {
        if (Character.isDigit(c) != TRUE) { // illegal input, declared "dead" below
            return 2;
        }

        switch (state) {
            case 0:  return 1;
            case 1:  return 1;
            default: return 2; // garbage state, declared "dead" below
        }
    }
    public boolean isGoalState(int state) {
        return (state == 1);
    }
    public boolean isDeadState(int state) {
        return (state == 2);
    }
}

class BooleanAcceptor extends GenAcceptor {
    
	public String lexClass() {
        return "BOOLEAN";
    }
    public int totalStates() {
        return 10;
    }
    public int nextState (char c, int state) {
        switch (state) {
            case 0: if(c == 'T' || c == 't'){
            	return 1;
            } else if(c == 'F' || c == 'f'){
            	return 5;
            } else {
            	return 9;
            }
            case 1: if(c == 'R' || c== 'r'){
            	return 2;
            } else{
            	return 9;
            }
            case 2: if(c == 'U' || c == 'u'){
            	return 3;
            }else{
            	return 9;
            }
            case 3: if(c == 'E' || c == 'e'){
            	return 4;
            }else{
            	return 9;
            }
            case 4: if(c == ""){
            	return 4;
            }else{
            	return 9;
            }
            case 5: if(c == 'A' || c == 'a'){
            	return 6;
            }else{
            	return 9;
            }
            case 6: if(c == 'L' || c == 'l'){
            	return 7;
            }else{
            	return 9;
            }
            case 7: if(c == 'S' || c == 's'){
            	return 8;
            }else{
            	return 9;
            }
            case 8: if(c == 'E' || c == 'e'){
            	return 4;
            } else{
            	return 9;
            }
            default: return 9; // garbage state, declared "dead" below
        }
    }
    public boolean isGoalState(int state) {
        return (state == 4);
    }
    public boolean isDeadState(int state) {
        return (state == 9);
    }
}

class SymAcceptor extends GenAcceptor {
    
	public String lexClass() { // needs to be changed
        return "SYM";
    }
    public int totalStates() {
        return 3;
    }
    public int nextState (char c, int state) {
        switch (state) {
            case 0:  if(c == '!' || c == '#' || c == '$' || c == '%' || c == '&' || 
            c == '*' || c == '+' || c == '.' || c == '/' || c == '<' || 
            c == '=' || c == '>' || c == '?' || c == '@' || c == '\\' ||
            c == '^' || c == '|' || c == '-' || c == '~' || c == ':'){
            	return 1;
            }else{
            	return 2;
            }
            default: return 2; // garbage state, declared "dead" below
        }
    }
    public boolean isGoalState(int state) {
        return (state == 1);
    }
    public boolean isDeadState(int state) {
        return (state == 2);
    }
}

class WhitespaceAcceptor extends GenAcceptor {
    
	public String lexClass() {
        return "";
    }
    public int totalStates() {
        return 3;
    }
    public int nextState (char c, int state) {
        switch (state) {
            case 0:
                if (c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\f') {
                    return 1;
                } else {
                    return 2;
                }
            default:
                return 2;
        }
    }
    public boolean isGoalState(int state) {
        return (state == 1);
    }
    public boolean isDeadState(int state) {
        return (state == 2);
    }
}

class CommentAcceptor extends GenAcceptor {
    
	public String lexClass() {
        return "";
    }
    public int totalStates() {
        return 6;
    }
    public int nextState (char c, int state) {
    	
        switch (state) {
            case 0:  
            if (c == '-'){
            	return 1;
            } else{
            	return 3;
            }
            case 1:  
            if (c == '-'){
            	return 2;
            } else {
            	return 3;
            }
            case 2: if(c != '!' && c != '#' && c != '$' && c != '%' && c != '&' && 
                    c != '*' && c != '+' && c != '.' && c != '/' && c != '<' && 
                    c != '=' && c != '>' && c != '?' && c != '@' && c != '\\' &&
                    c != '^' && c != '|' && c != '-' && c != '~' && c != ':'){
            	return 3;
            }else if(c == '-'){
            	return 4;
            }else{
            	return 5;
            }
            case 3: if(c != '\n'){
            	return 3;
            }else{
            	return 5;
            }
            case 4: if(c == '-'){
            	return 4;
            }else{
            	return 5;
            }
            default: return 5; // garbage state, declared "dead" below
        }
    }
    public boolean isGoalState(int state) {
        return (state == 3 || state == 4);
    }
    public boolean isDeadState(int state) {
        return (state == 5);
    }
}

class TokAcceptor extends GenAcceptor {

    String tok;
    int tokLen;

    TokAcceptor (String tok) {
        this.tok = tok;
        tokLen = tok.length();
    }
    
    char tokArray[] = tok.toCharArray();
    
    public String lexClass() {
        return tok;
    }
    public int totalStates() {
        return (tokLen+2);
    }
    public int nextState (char c, int state) {
    	if (tok != "Integer" && tok != "Boolean" && tok != "if" && tok != "then" && tok != "else" && tok != "(" && tok != ")" && tok != ";"){
    	    return (tokLen+1);
    	}
    	for(i=0, i<tokLen, i++){
    		switch (state) {
            case i: 
            	if(i == (tokLen-1) && c==tokArray[i]){
				    return tokLen;
				}else if (c==tokArray[i]){
            		return i+1;
            	}else{
            		return (tokLen+1);
            	}	
            default: return (tokLen+1); // garbage state, declared "dead" below
            }
        }
    	}
        
    }
    public boolean isGoalState(int state) {
        return (state == (tokLen));
    }
    public boolean isDeadState(int state) {
        return (state == (tokLen+1));
    }
}


public class MH_Lexer extends GenLexer implements LEX_TOKEN_STREAM {

	static DFA varAcceptor = new VarAcceptor() ;
	static DFA numAcceptor = new NumAcceptor() ;
	static DFA booleanAcceptor = new BooleanAcceptor() ;
	static DFA symAcceptor = new SymAcceptor() ;
	static DFA whitespaceAcceptor = new WhitespaceAcceptor() ;
	static DFA commentAcceptor = new CommentAcceptor() ;
	
	static DFA intAcceptor = new TokAcceptor("Integer") ;
	static DFA boolAcceptor = new TokAcceptor("Boolean") ;
	static DFA ifAcceptor = new TokAcceptor("if") ;
	static DFA thenAcceptor = new TokAcceptor("then") ;
	static DFA elseAcceptor = new TokAcceptor("else") ;
	
	static DFA lbraAcceptor = new TokAcceptor("(") ;
	static DFA rbraAcceptor = new TokAcceptor(")") ;
	static DFA semcolAcceptor = new TokAcceptor(";") ;
	static DFA[] acceptors = new DFA[] {varAcceptor, numAcceptor, booleanAcceptor, symAcceptor, whitespaceAcceptor, commentAcceptor, intAcceptor, boolAcceptor, ifAcceptor, thenAcceptop, elseAcceptop, lbraAcceptor, rbraAcceptor, semcolAcceptor};

    MH_Lexer (Reader reader) {
        super(reader, acceptors);
    }

}

