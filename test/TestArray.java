public class TestArray {
    public static void main(String[] args) {
        int[] a = new int[5];
        a[0] = 1;
        a[1] = 3;
        a[2] = 2;
        a[3] = 5;
        a[4] = 4;
        printArray(a);
        sort(a);
        printArray(a);
    }

    private void printArray(int[] array) {
        int len = array.length;
        int i = 0;
        for (i = 0; i < len; i = i + 1) {
            System.out.println(array[i]);
        }
    }

    private void sort(int[] array) {
        int len = array.length;
        int i = 0;
        int j = 0;
        int temp = 0;
        for (i = 0; i < len - 1; i = i + 1) {
            for (j = 0; j < len - i - 1; j = j + 1) {
                if (array[j + 1] < array[j]) {
                    temp = array[j];
                    array[j] = array[i];
                    array[i] = temp;
                }
            }
        }
    }
}