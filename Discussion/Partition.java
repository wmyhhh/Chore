public class Partition {
    public static IntList[] partition(IntList lst, int k){
        IntList[] array = new IntList[k];
        int index = 0;
        // reverse the list and return the head pointer
        IntList L = reverse(lst);

        while (L != null){
            IntList next = L.rest;

            // head insertion(prepend)
            L.rest = array[index];
            array[index] = L;

            L = next;
            index = (index + 1) % k;
        }
        return array;
    }
}
