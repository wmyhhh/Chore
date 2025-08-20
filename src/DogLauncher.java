public class DogLauncher {

    public static void main(String[] args){
        /*
        Dog smalldog;   // declaration of a dog variable
        new Dog(20);    // instantiation of the dog class as a dog object
        smalldog = new Dog(5);  // instantiation and assignment
        Dog hugedog = new Dog(500);   // declaration, instantiation and assignment
        smalldog.makeNoise();
        hugedog.makeNoise();    //invocation of the makeNoise method
        */
        Dog d1 = new Dog(40);
        Dog d2 = new Dog(75);
        Dog bigger = Dog.maxDog(d1, d2);    // static calls on Dog class
        Dog larger = d1.compareDog((d2));   // non-static calls on the instance
        bigger.makeNoise();
        larger.makeNoise();
        System.out.println(Dog.binomen);
        Dog[] manyDogs = new Dog[4];    // create an array
        manyDogs[0] = d1;
        manyDogs[1] = d2;
    }


}