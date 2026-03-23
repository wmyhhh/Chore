public class DogProblem {
    public static Dog[] biggerThanNeighbor(Dog[] d){
        int cnt = 0;
        Dog[] result = new Dog[d.length];
        for (int i=0; i<d.length; i++){
            if (isBiggest(d, i)){
                result[cnt] = d[i];
                cnt++;
            }
        }
        result = arrayWithoutNull(result, cnt);
        return result;
    }
    public static boolean isBiggest(Dog[] d, int i){
        boolean judge = true;
        for (int j=-2; j<=2; j++){
            if (isValid(d, i+j)){
                if (j==0){
                continue;
                }else if (d[i].weight < d[i+j].weight){
                    judge = false;
                }
            }
        }
        return judge;
    }
    public static boolean isValid(Dog[] d, int k){
        int l = d.length;
        if (k<0 || k>=l){
            return false;
        }
        return true;
    }
    public static Dog[] arrayWithoutNull(Dog[] d, int cnt){
        Dog[] newArray = new Dog[cnt];
        for (int i=0; i<cnt; i++){
            newArray[i] = d[i];
        }
        return newArray;
    }
    public static void main(String[] args){
        Dog[] Dogs = new Dog[8]; 
        Dogs[0] = new Dog(5);
        Dogs[1] = new Dog(15);
        Dogs[2] = new Dog(5);
        Dogs[3] = new Dog(25);
        Dogs[4] = new Dog(35);
        Dogs[5] = new Dog(15);
        Dogs[6] = new Dog(35);
        Dogs[7] = new Dog(25);
        Dog[] d = biggerThanNeighbor(Dogs);
        for (int i=0; i<d.length; i++){
            System.out.print(d[i].weight + " ");
        }
        System.out.println();
    }
    
}
