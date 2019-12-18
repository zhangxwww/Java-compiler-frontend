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
        exp = (exp + "#");
        Stack opSt = new Stack();
        opSt.push("#");
        String reversePolish = "";
        int i = 0;
        String ch = nextToken(exp, i);
        while(!(opSt.empty())){
            if (isOp(ch)){
                if((ch.charAt(0)) == '('){
                    opSt.push(ch);
                }else if((ch.charAt(0)) == ')'){
                    String topChar = opSt.pop().toString();
                    while ((topChar.charAt(0)) != '('){
                        reversePolish = (reversePolish+topChar);
                        topChar = opSt.pop().toString();
                    }
                }else {
                    String topChar = opSt.pop().toString();
                    opSt.push(topChar);
                    while (precede(topChar, ch)) {
                        reversePolish = reversePolish + topChar;
                        topChar = opSt.pop().toString();
                        topChar = opSt.pop().toString();
                        opSt.push(topChar);
                    }
                    if (ch.charAt(0) != '#') {
                        opSt.push(ch);
                    }
                }
            }else{
                reversePolish = (reversePolish + ch + " ");
            }
            if( ch.charAt(0) != '#'){
                int len = ch.length();
                i = (i+len);
                ch = nextToken(exp, i);
            }else{
                ch = opSt.pop().toString();
            }
        }
        return reversePolish;
    }
    
    public static int computeReversePolish(String rpExp){
        rpExp = (rpExp + "#");
        int i = 0;
        Stack st = new Stack();
        String token = nextToken(rpExp, i);
        while(token.charAt(0) != '#'){
            int len = token.length();
            i = (i+len);
            if(isOp(token)){
                String s1 = st.pop().toString();
                int i1 = Integer.parseInt(s1);
                String s2 = st.pop().toString();
                int i2 = Integer.parseInt(s2);
                if(token.charAt(0) == '+'){
                    int i3 = (i2+i1);
                    st.push(i3);
                }else if(token.charAt(0) == '-'){
                    int i3 = (i2-i1);
                    st.push(i3);
                }else if(token.charAt(0) == '*'){
                    int i3 = (i2*i1);
                    st.push(i3);
                }else if(token.charAt(0) == '/'){
                    int i3 = i2/i1;
                    st.push(i3);
                }
            }else{
                st.push(token);
                i = (i+1);
            }
            token = nextToken(rpExp, i);
        }
        String res = st.pop().toString();
        int rtn = Integer.parseInt(res);
        return rtn;
    }


    public static void main(String[]  args){
        System.out.println(infixToReversePolishExp("21*5+(6-4/4)*2-(100*52)"));
        System.out.println(computeReversePolish(infixToReversePolishExp("21*5+(6-4/4)*2-(100*52)")));
        System.out.println(infixToReversePolishExp("a*b+(c-d/e)*f-(42*52)"));
    }
}