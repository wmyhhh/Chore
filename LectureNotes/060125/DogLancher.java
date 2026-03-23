public class DogLancher {
    public static void main(String[] args){
        Dog d1 = new Dog(2);
        Dog d2 = new Dog(100);
        d1.makeNoise();
        /* 
        Dog d = Dog.maxDog(d1, d2);
        d.makeNoise();
        Dog dd = d2.minDog(d1);
        dd.makeNoise();
        */
        Dog.maxDog(d1, d2).makeNoise();
        d2.minDog(d1).makeNoise();
    }
}
