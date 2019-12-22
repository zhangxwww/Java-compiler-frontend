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
        int size = 2*exp.length();
        Object[] opSt = new Object[size+10];
        int topPos = -1;
        int i = 0;
        String topChar = "";
        String ch = "";
        int len = 0;
        Object top = "";
        exp = exp+"#";
        ch = nextToken(exp, i);
        topPos = topPos + 1;
        opSt[topPos] = "#";
        while(topPos >= 0){
            if (isOp(ch)){
                if(ch.charAt(0) == '('){
                    topPos = topPos+1;
                    opSt[topPos] = ch;
                }
                if(ch.charAt(0) == ')'){
                    top = opSt[topPos];
                    topPos = topPos - 1;
                    topChar = top.toString();
                    while (topChar.charAt(0) != '('){
                        reversePolish = (reversePolish+topChar);
                        top = opSt[topPos];
                        topPos = topPos - 1;
                        topChar = top.toString();
                    }
                }
                if(ch.charAt(0) != '(') {
                    if(ch.charAt(0) != ')'){
                        top = opSt[topPos];
                        topPos = topPos - 1;
                        topChar = top.toString();
                        topPos = topPos + 1;
                        opSt[topPos] = topChar;
                        while (precede(topChar, ch)) {
                            reversePolish = reversePolish + topChar;
                            top = opSt[topPos];
                            topPos = topPos - 1;
                            topChar = top.toString();
                            top = opSt[topPos];
                            topPos = topPos - 1;
                            topChar = top.toString();
                            topPos = topPos + 1;
                            opSt[topPos] = topChar;
                        }
                        if (ch.charAt(0) != '#') {
                            topPos = topPos + 1;
                            opSt[topPos] = ch;
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
                top = opSt[topPos];
                topPos = topPos - 1;
                ch = top.toString();
            }
        }
        return reversePolish;
    }

    public static float computeReversePolish(String rpExp){
        int i = 0;
        int size = 2*rpExp.length();
        Object[] st = new Object[size+10];
        int topPos = -1;
        String token = "";
        String res = "";
        String s1 = "";
        String s2 = "";
        float i1 = 0;
        float i2 = 0;
        float i3 = 0;
        float rtn = 0;
        int len = 0;
        Object top = "";
        rpExp = rpExp + "#";
        token = nextToken(rpExp, i);
        while(token.charAt(0) != '#'){
            len = token.length();
            i = (i+len);
            if(isOp(token)){
                top = st[topPos];
                s1 = top.toString();
                topPos = topPos - 1;
                top = st[topPos];
                s2 = top.toString();
                topPos = topPos - 1;
                i1 = Float.parseFloat(s1);
                i2 = Float.parseFloat(s2);
                if(token.charAt(0) == '+'){
                    i3 = i2+i1;
                    topPos = topPos + 1;
                    st[topPos] = i3;
                }
                if(token.charAt(0) == '-'){
                    i3 = i2-i1;
                    topPos = topPos + 1;
                    st[topPos] = i3;
                }
                if(token.charAt(0) == '*'){
                    i3 = i2*i1;
                    topPos = topPos + 1;
                    st[topPos] = i3;
                }
                if(token.charAt(0) == '/'){
                    i3 = i2/i1;
                    topPos = topPos + 1;
                    st[topPos] = i3;
                }
            }else{
                topPos = topPos + 1;
                st[topPos] = token;
                i = i+1;
            }
            token = nextToken(rpExp, i);
        }
        top = st[topPos];
        topPos = topPos - 1;
        res = top.toString();
        rtn = Float.parseFloat(res);
        return rtn;
    }

    public static void main(String[]  args){
        System.out.println(computeReversePolish(infixToReversePolishExp("21*5+(6-4/4)*2-(100*52)")));
        System.out.println(computeReversePolish(infixToReversePolishExp("4444*34330/5+3*3/2-(2*3/5/23234)")));
        System.out.println(computeReversePolish(infixToReversePolishExp("4444*(34+2)/(5-1)+5/(23234-2333)")));
    }

}