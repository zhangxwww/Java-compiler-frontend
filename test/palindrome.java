public class Palindrome {

    String welcome = "Hello world";

	public static void main(String[] args) {
		String s = input();
		int len = s.length();
		int mid = len / 2;
		int i = 0;
		for (i = 0; i < mid; i = i + 1) {
			if (s.charAt(i) != s.charAt(len - i - 1)) {
				System.out.println("False");
				return;
			}
		}
		System.out.println("True");
	}

	private int hello(int a, int b) {
	    int c = a + b;
	    c = c - (1 * a) + b;
	    System.out.println(c);
	    return c;
	}

	private void hey() {
        welcome = "HEY";
        hello(1, 2);
	    return;
	}
}