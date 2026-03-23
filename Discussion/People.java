public class People {
    public class Person {
        void speakTo(Person other) { System.out.println("kudos"); }
        void watch(SoccerPlayer other) { System.out.println("wow"); }
    }
    public class Athlete extends Person {
        void speakTo(Athlete other) { System.out.println("take notes"); }
        void watch(Athlete other) { System.out.println("game on"); }
    }
    public class SoccerPlayer extends Athlete {
        void speakTo(Athlete other) { System.out.println("respect"); }
        void speakTo(Person other) { System.out.println("hmph"); }
    }

    public static void main(String[] args){
        Person itai = new Person(); // fine
        SoccerPlayer shivani = new Person(); //CE
        Athlete sohum = new SoccerPlayer(); // fine
        Person jack = new Athlete(); // fine
        Athlete anjali = new Athlete();  // fine
        SoccerPlayer chirasree = new SoccerPlayer();  // fine
        itai.watch(chirasree);  // "wow"
        jack.watch(sohum);  // CE person static type not soccer player
        itai.speakTo(sohum); // CE person cannot speak to athlete
        jack.speakTo(anjali); // CE person cannot speak to athlete
        anjali.speakTo(chirasree); // CE athlete cannot speak to soccer player
        sohum.speakTo(itai); // "kudo"
        chirasree.speakTo((SoccerPlayer) sohum); // CE soccer player cannot speak to soccer player
        sohum.watch(itai); // CE person cannot be watched
        sohum.watch((Athlete) itai); // RE dynamic type not an athlete
        ((Athlete) jack).speakTo(anjali); // "take notes"
        ((SoccerPlayer) jack).speakTo(chirasree); // "wow"
        ((Person) chirasree).speakTo(itai); // "hmph"

        // correction
        Person itai = new Person();
        SoccerPlayer shivani = new Person(); // CE
        Athlete sohum = new SoccerPlayer();
        Person jack = new Athlete();
        Athlete anjali = new Athlete();
        SoccerPlayer chirasree = new SoccerPlayer();
        itai.watch(chirasree); // wow
        jack.watch(sohum); // CE
        itai.speakTo(sohum); // kudos
        jack.speakTo(anjali); // kudos
        anjali.speakTo(chirasree); // take notes
        sohum.speakTo(itai); // hmph
        chirasree.speakTo((SoccerPlayer) sohum); // respect
        sohum.watch(itai); // CE
        sohum.watch((Athlete) itai); // RE
        ((Athlete) jack).speakTo(anjali); // take notes
        ((SoccerPlayer) jack).speakTo(chirasree); // RE
        ((Person) chirasree).speakTo(itai); // hmph
    }
}
