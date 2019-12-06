public class Palindrome {
	public static void main(String[] args) {
		String s = input();
		int len = s.length;
		int mid = s / 2;
		int i = 0;
		for (i = 0; i < mid; i = i + 1) {
			if (s.charAt(i) != s.charAt(len - i - 1)) {
				System.out.println("False");
				return;
			}
		}
		System.out.println("True");
	}
}