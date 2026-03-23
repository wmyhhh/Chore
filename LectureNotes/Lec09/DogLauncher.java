import java.util.Comparator;

public class DogLauncher {
    public static void main(String[] args){
        Dog d1 = new Dog(40, "husky");
        Dog d2 = new Dog(60, "alaska");
        Dog d3 = new Dog(70, "labordudo");
        Dog d4 = new Dog(20, "poodle");

        Dog[] d = new Dog[]{d1, d2, d3, d4};
        Dog dm = (Dog)Maximizer.max(d);
        dm.bark();

        Comparator<Dog> nc = Dog.getNameComparator();
        if (nc.compare(d1, d3) > 0){
            d1.bark();
        }else{
            d2.bark();
        }
    }
}
