import java.util.Stack;

public class TestExpEval {

    public static boolean isOp(String c){
        char tmp = c.charAt(0);
        if(tmp == '+'){
            return true;
        }
        if(tmp == '-'){
            return true;
        }
        if(tmp == '*'){
            return true;
        }
        if(tmp == '/'){
            return true;
        }
        if(tmp == '('){
            return true;
        }
        if(tmp == ')'){
            return true;
        }
        if(tmp == '#'){
            return true;
        }
        return false;
    }

    public static boolean precede(String op1, String op2){
        char tmp1 = op1.charAt(0);
        char tmp2 = op2.charAt(0);
        if(tmp1 == '('){
            return false;
        }
        if(tmp1 == '#'){
            return false;
        }
        if(tmp2 == '#'){
            return true;
        }
        if(tmp1 == '+'){
            if(tmp2 == '*'){
                return false;
            }
            if(tmp2 == '/'){
                return false;
            }
        }
        if(tmp1 == '-'){
            if(tmp2 == '*'){
                return false;
            }
            if(tmp2 == '/'){
                return false;
            }
        }
        return true;
    }

    public static String nextToken(String str, int startIdx){
        int len = str.length();
        String res = "";
        if(isOp(str.substring(startIdx, startIdx + 1))){
            return str.substring(startIdx, startIdx + 1);
        }
        while(startIdx < len){
            if(isOp(str.substring(startIdx, startIdx + 1))){
                break;
            }
            if(str.charAt(startIdx) == ' '){
                break;
            }
            res = (res + str.substring(startIdx, (startIdx + 1)));
            startIdx = (startIdx+1);

        }
        return res;
    }
    public static String infixToReversePolishExp(String exp){
        String reversePolish = "";
        Stack opSt = new Stack();
        int i = 0;
        String topChar = "";
        String ch = "";
        int len = 0;
        exp = exp+"#";
        ch = nextToken(exp, i);
        opSt.push("#");
        while(!(opSt.empty())){
            if (isOp(ch)){
                if(ch.charAt(0) == '('){
                    opSt.push(ch);
                }
                if(ch.charAt(0) == ')'){
                    top = opSt.pop();
                    topChar = top.toString();
                    while (topChar.charAt(0) != '('){
                        reversePolish = (reversePolish+topChar);
                        top = opSt.pop();
                        topChar = top.toString();
                    }
                }
                if(ch.charAt(0) != '(') {
                    if(ch.charAt(0) != ')'){
                        top = opSt.pop();
                        topChar = top.toString();
                        opSt.push(topChar);
                        while (precede(topChar, ch)) {
                            reversePolish = reversePolish + topChar;
                            top = opSt.pop();
                            topChar = top.toString();
                            top = opSt.pop();
                            topChar = top.toString();
                            opSt.push(topChar);
                        }
                        if (ch.charAt(0) != '#') {
                            opSt.push(ch);
                        }
                    }
                }
            }else{
                reversePolish = (reversePolish + ch + " ");
            }
            if( ch.charAt(0) != '#'){
                len = ch.length();
                i = (i+len);
                ch = nextToken(exp, i);
            }else{
                top = opSt.pop();
                ch = top.toString();
            }
        }
        return reversePolish;
    }
}