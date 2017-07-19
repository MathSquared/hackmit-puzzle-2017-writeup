# How I solved the HackMIT 2017 admissions puzzle

*Alex Meed*

Is it strange that I've never been to a hackathon?

After all, I've been programming since my sophomore year of high school. I study computer science. I've done two internships and more programming contests than I can count. But I've never been to a hackathon.

The HackMIT admissions puzzles, though, piqued my interest. Usually, to get into HackMIT, you have to fill out an application that's strong enough for the organizers to want to admit you. But, being hackathon hosts, they weren't satisfied with such a mundane approach. So, as you could expect from a bunch of nerds, every year the organizers publish a set of technical puzzles to work through. The first 50 to solve get guaranteed admission to HackMIT.

I don't know what drove me to give the puzzles a shot&mdash;after all, I didn't think my first hackathon would be in Massachusetts. But the evening after I found out about them, I sat down at my laptop, typed `mkdir hackmit-puzzle-2017` in my home directory, registered on the puzzle website, and got to work.

I started the puzzles a few days after they were published&mdash;I didn't learn that they existed until then. But somehow, I managed to figure them out quickly enough to get one of those coveted 50&nbsp;slots.

As I solved all of the puzzles, I kept near-stream-of-consciousness logs of everything I did. Now that I've finished solving everything, I've written up my approaches to the challenges in what I hope is a digestible, streamlined format. I've omitted some (but not all) of the meandering paths I went down and taken a bit of artistic license with the order I did things in, just to make things easier to follow, but this is still substantially the thought process I went through for each problem. I'm also publishing most of the files I downloaded and generated to solve the puzzles, including all the code I wrote and every single one of those logs. I'm hoping that what I'm publishing, along with the official writeup, is useful to you.

So: how I got into HackMIT, in five vignettes.

## Puzzle 1: `warp`

I'm naming the puzzles after their third-level domains under the main puzzle website, `delorean.codes`. After you log into the site and hit the Launch button, you're sent to the first puzzle, at `warp.delorean.codes`. So it begins.

The first screen you see when you load the starting puzzle is a mangled version of the HackMIT home page. And it's in a strange font, too.

### Step 1: decrypt the website

First, I tried to get rid of the strange font. That was easy; just view the source of the page. Or, it would have been easy, except that the source code was still gibberish. Even the JavaScript at the bottom was unreadable (and threw an amusing syntax error in the console as a result).

Fortunately, we had a starting point that we can use to try to decipher this: the real HackMIT home page. Everything was the same layout, and it looked like none of the words have changed length. Plus, characters that were the same on the original website (like the two Rs in "REGISTER") were the same in the mangled version. It looked like the puzzle setters just ran the HackMIT homepage through some sort of *substitution cipher*: every letter in the ciphertext (what I was seeing) translated to exactly one letter in the plaintext (the deciphered version).

I started deciphering the page manually, keeping a table of ciphertext-to-plaintext mappings, and quickly figured out it was a simple *shift cipher*. You could decipher a letter by adding 15 to its position in the alphabet, wrapping around; for instance, A translated to P, B to Q, and so forth. Using that, I extrapolated to find the rest of the cipher table, and then wrote a bash one-liner to decipher arbitrary text quickly.

On the left of the big HackMIT logo, there was a weird-looking string with some slashes in it. Maybe it was a link of some sort? I deciphered it, and noticed it was a link to a JAR file, which I promptly downloaded.

### Step 2: crack the Java program

Not having anything else to do with the JAR file, I just ran it:

    $ java -jar dl.jar
    It's not your time ;)
    $

Okay, that's not going to work. Let's take a look inside.

The big secret of JAR files is that they're just ZIP archives with a special structure. So, I unzipped the JAR to find two Java `.class` files&mdash;`WarpCLI` and `WarpCLI$1`, an anonymous class inside of `WarpCLI`&mdash;along with some metadata (which we didn't care about).

Now that I had the class files, I was curious about their structure. Any Java installation has a command called *`javap`*, which prints out all of the method signatures of a `.class` file. I used that to investigate the two classes I'd downloaded:

    $ javap WarpCLI
    Compiled from "WarpCLI.java"
    public class WarpCLI {
      public WarpCLI();
      public static void main(java.lang.String[]);
    }
    $ javap 'WarpCLI$1'
    Compiled from "WarpCLI.java"
    final class WarpCLI$1 {
      int t;
      WarpCLI$1();
      public java.lang.String toString();
    }
    $

Not as insightful as I'd hoped.

At this point, a reasonable person would probably just decompile the classes and fiddle with the code enough to get it to work. I thought of this, but&mdash;and this is the only reason why I didn't do that&mdash;*I couldn't pick a decompiler to use*. So, I went on an adventure into something I was only vaguely familiar with: *Java bytecode*.

If you've taken a systems class, you know that programs in a language like C++ are compiled to machine code, which is a bunch of numbers in hexadecimal. The CPU knows how to run machine code, but it's also specific to a particular kind of CPU: for instance, an x86 processor (which probably runs in your desktop computer) can't run a program written in machine code for an ARM (a common mobile CPU). That means machine-code programs are platform-dependent; you can only run them on one kind of computer.

The whole idea behind Java is that it's platform-independent; the code you write will run on any computer that can run Java. (Java's mantra for this is "*write once, run anywhere*".) So, instead of running directly on the CPU, Java runs on the *Java Virtual Machine* (JVM). The JVM is a standardized architecture for a hypothetical computer; your computer's Java install emulates the JVM whenever it runs a Java program. The JVM has its own machine code in a sense, but we don't call it machine code since the machine it's written for doesn't exist. Instead, since it's structured as a bunch of bytes, we call it bytecode. Just like a C++ compiler turns C++ source code into machine code for a given processor, a Java compiler turns Java source code into Java bytecode.

Now that we know what bytecode is, how do we use that knowledge? The `javap` command takes a `-c`&nbsp;option, which spits out not only the method signatures, but also the bytecode for each method. That's what I did next:

    $ javap -c WarpCLI
    Compiled from "WarpCLI.java"
    public class WarpCLI {
      public WarpCLI();
        Code:
           0: aload_0
           1: invokespecial #1                  // Method java/lang/Object."<init>":()V
           4: return

      public static void main(java.lang.String[]);
        Code:
           0: invokestatic  #2                  // Method java/time/Instant.now:()Ljava/time/Instant;
           3: astore_1
           4: ldc2_w        #4                  // long 2172847386l
           7: invokestatic  #6                  // Method java/time/Instant.ofEpochSecond:(J)Ljava/time/Instant;
          10: astore_2
          11: aload_2
          12: lconst_1
          13: getstatic     #7                  // Field java/time/temporal/ChronoUnit.DAYS:Ljava/time/temporal/ChronoUnit;
          16: invokevirtual #8                  // Method java/time/Instant.plus:(JLjava/time/temporal/TemporalUnit;)Ljava/time/Instant;
          19: astore_3
          20: aload_1
          21: aload_2
          22: invokevirtual #9                  // Method java/time/Instant.isAfter:(Ljava/time/Instant;)Z
          25: ifeq          55
          28: aload_1
          29: aload_3
          30: invokevirtual #10                 // Method java/time/Instant.isBefore:(Ljava/time/Instant;)Z
          33: ifeq          55
          36: getstatic     #11                 // Field java/lang/System.out:Ljava/io/PrintStream;
          39: new           #12                 // class WarpCLI$1
          42: dup
          43: invokespecial #13                 // Method WarpCLI$1."<init>":()V
          46: invokevirtual #14                 // Method WarpCLI$1.toString:()Ljava/lang/String;
          49: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
          52: goto          63
          55: getstatic     #11                 // Field java/lang/System.out:Ljava/io/PrintStream;
          58: ldc           #16                 // String It's not your time ;)
          60: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
          63: return
    }
    $

(I also disassembled the `WarpCLI$1` class, but the result was hundreds of lines long and not necessary to solve the problem. Just take my word for it that its `toString` method gives us the solution.)

That's kind of a lot, but you don't need to know too much about bytecode to understand it. Each line is an instruction in Java bytecode, labeled with its decimal address. The numbers that start with # point to constants or symbols that are packaged with the class file. (The disassembler helpfully prints out what they correspond to in the comments on the right.) The numbers that don't start with # are addresses of other instructions.

If you're wondering why the instructions have so few operands compared to, say, x86 assembly, that's because Java bytecode is *stack-based*. Normal CPUs are *register-based*; they keep a stack in memory and a few special variables, called registers. Operations can pull from memory or from these registers. In Java bytecode, there are no registers&mdash;everything's kept on the stack. Instructions always act on the top few things on the stack, and push their results back onto the stack. That means you don't need to tell a Java bytecode instruction what it's operating on, because it just pulls from the stack. It's a bit hard to get used to, but that's how it works.

This is a high-level view of Java bytecode, and probably subtly inaccurate, but it's all you need to know to understand this solution (it's all I needed to know to solve the problem).

Once you know that, you can kind of figure out what this code does. Instructions 0&ndash;19 get the current time and do some operations to it. The result of those is a bunch of `java.time.Instant` objects, which represent moments in time. (The `Ljava/time/Instant;` stuff is just how the Java Virtual Machine, or JVM, represents class types internally.) Instructions 20&ndash;25 compare two of the Instants, and if they're equal, branch to instruction&nbsp;55. Instructions 28&ndash;33 do the same to two other Instants. If neither of those branches fire, instructions 36&ndash;52 construct a new `WarpCLI$1`, call its `toString` method, and print the result. If one of the earlier branches did fire, instructions 55&ndash;60 print the string `"It's not your time ;)"` that we saw earlier.

Our goal is to get to instructions 36&ndash;52; that is, to skip the branches at lines 25&nbsp;and&nbsp;33. One way to do that is to just turn them into no-ops&mdash;strangely enough, though, I couldn't figure out the opcode for that. Plus, if you replace an instruction with one that doesn't push or pop the exact same number of things, you run the risk of screwing up the stack layout, and then the JVM will complain. So, the next-best alternative, and the one I did, is to twiddle the branch instructions between `ifeq` and `ifne` until one of the combinations works. There are only two branch instructions, so only 2<sup>2</sup>&nbsp;=&nbsp;4 possibilities! Easy!

In order to twiddle opcodes, I hexdumped `WarpCLI.class`, then wrote a short bash script to unhexdump it and run the result. Now, I could essentially edit the class file in a text editor. Then, I had to find the bytes to twiddle. I used the Internet to find the opcode for `ifeq`, which is&nbsp;`0x99`; luckily, that byte only appeared in two places in my hexdump, corresponding to the two `ifeq` instructions. I flipped one, then the other, then both to the `ifne` instruction (opcode&nbsp;`0x9a`), and finally got it to output the solution.

## Puzzle 2: `store`

I opened the next puzzle and found a login form staring me in the face. Not knowing the password, I went for the only logical approach: hack the store. I've taken a security class or two, so I was pretty familiar with the typical security holes that appear in websites.

### Step 1: breach the login page

Puzzle 1 taught me to look at the HTML source for the page, so I did, and found a comment about terminating early if `a[i] != b[i]`. I wasn't exactly sure what that meant, but it reminded me of an insecure way of comparing passwords that's vulnerable to a *timing attack*.

A timing attack is a way of gaining extra information from a program by measuring how much time it takes to do something. In this case, we can exploit the time a string comparison takes. Here's what a vulnerable string equality method might look like in C++:

    bool streq(char* a, char* b) {
        int i = 0;
        while (a[i] != '\0' || b[i] != '\0') {
            if (a[i] != b[i])
                return false;  // stop comparison early
            i++;
        }
        return true;
    }

This is fairly simple, despite the tiny bit of pointer magic. It compares the two strings, character by character. At each index&nbsp;`i`, if the two characters differ, we stop early and return false; there's no reason to keep going if we already know the strings are different. If we hit the end of both strings simultaneously, as indicated by the null character at the end, we return true, indicating that the strings are equal. (If one string is shorter than the other, there'll be an index&nbsp;`i` where `a[i]` will be the null character and `b[i]` won't be, or vice versa, so `a[i] != b[i]` and we terminate early and return false.)

So, this `streq` method is *correct*, but it's *insecure*. Let's say each memory access takes 100&nbsp;ns. (That's a lot slower than RAM actually is, but we'll go with it for now.) That means each iteration of the `while` loop takes 400&nbsp;ns.

Think about what that means. If the strings differ at the first character, the loop stops after one iteration and returns false. Total time: 400&nbsp;ns. But if the first characters are the same, it does an extra iteration. Now, if the second character is different, the program takes 400&nbsp;ns more, for a total of 800&nbsp;ns. You can see a pattern here: the more characters at the start of the strings are the same, the longer the check takes.

Now let's apply this to hacking the store. If the hypothetical people who wrote this site don't know how to properly store passwords, they might just put them in the database in plain text, and call that `streq` method to check any password a user enters. (Here, the "hypothetical people who wrote this site" are not the HackMIT organizers, but the people they're trying to emulate who would have programmed the web store and put that comment in the source code.) So, let's say `a` is whatever password the user sends to the site, and `b` is the real password. So, the more characters at the start of the guess match the actual password, the longer the check will take.

Here's the big insight: if we can measure how long the check takes, we can try every first character and watch for which comparison takes a longer time. Then, since that comparison took longer, there were more characters at the front that were correct. So we save the first character of that guess as the real first character, and move to try every possibility for the second character. This way, instead of having to brute-force every possible password, we can brute-force each character before moving on to the next. Instead of 62<sup>12</sup> possible passwords (62 symbols in 12 positions), now we only have 62&times;12 to check. If you don't grasp how huge that is, those two numbers differ by about a factor of 4.336&times;10<sup>18</sup>!

I initially tried to directly apply the timing attack concept; I wrote a Python script that uses `curl` to attempt a login, trying every valid first character of a password, and prints out the time it took. But the times I was getting were too noisy to be of any use&mdash;they would be several seconds apart even if the actual comparison took the same amount of time. Clearly, this was not going to work.

Defeated, I tried a few other approaches. One thing I attempted was opening a `netcat` session and typing in one character of the password at a time, hoping it would immediately close the connection after seeing one bad character. But it seemed like the server waited until the client sent the whole query, so I had the wrong approach.

While I was looking over the results of that attempt, though, I noticed an interesting HTTP response header:

    X-Upstream-Response-Time: 0.01

So it looks like this server is a *reverse proxy*: it delegates the password comparison to some other service, waits for the result, then feeds it back to us. `X-Upstream-Response-Time` must be how long that other service took. Presumably, the web server and the upstream service have a pretty good Internet connection to each other, so maybe this header would be less noisy than actually measuring how long the request takes from my laptop.

I updated the Python script to use the HTTP header, and ran it again. At first, I saw an endless string of&nbsp;`0.01`s. When the script tried a password starting with&nbsp;*2*, though, it hit the jackpot:

    X-Upstream-Response-Time: 0.51

(Half a second? That must be a *really* slow upstream service.)

I repeated this approach, and eventually upgraded my program to use multithreading to try all 62&nbsp;options faster. Eventually, my program threw an exception, which was probably because the `X-Upstream-Response-Time` header had disappeared. I tried the password that caused the exception and successfully logged in.

### Step 2: buy the solution

When I got into the site, I was politely informed I would need 1000&nbsp;HackCoins to buy a solution to the problem.

My balance: 50.

Oh, well. I could transfer my entire balance to the other account&mdash;which I did, then cracked its password too. Now the second account had 100&nbsp;coins, and the first one had&nbsp;0. No help.

Clearly, there wasn't enough money in the entire system for me to buy the solution. So, I would need to hack the store again, this time to generate the cash I needed.

First, I tried to transfer coins to myself. I opened my browser developer tools and changed the transfer dropdown to use my own username, then hit Transfer.

    you can't transfer to yourself

So that didn't work. I was too nervous to transfer to a random invalid username, fearing that I'd send all my money into the abyss.

Next, I thought about submitting a bunch of transfer requests in quick succession. Sometimes, websites won't check for this, and if they've designed the website badly, things might happen out of order or multiple times. In this case, I was hoping there would be a race condition where a bunch of transfer requests check the source account's balance before a single one of them actually withdraws the money. That would mean each one would think the account has the same nonzero balance, and they'd each load that amount into the destination account. The result: money duplication.

I logged into one of the accounts and hit Transfer twice. Then I checked the other account, which had a balance of&nbsp;200.

Double my old balance! I did it! I spammed the Transfer button on that account, changed back to the old one, and rejoiced at the sight of the solution.

As I later told someone who was stumped in a Slack DM:

    ameed: you have a button that gives you money (Transfer)
    ameed: what's the stupidest thing you could do if you want more money
    [redacted]: change the value
    [redacted]: ?
    ameed: think stupider
    ameed: I'm not a programmer
    ameed: Heck, I'm a seven-year-old
    ameed: I have a magic button that gives me money, and I want more money
    ameed: what do I do to the button
    [redacted]: repeatedly hit it :D?
    ameed: try that :D
    [redacted]: holy fuck

(I've included a few Slack logs like this so you can have better insight into my thought process and that of others&mdash;or just for humor. I've gotten permission from everyone whose chat logs appear here, and I told them I'd withhold their usernames, so I have.)

Who the heck programmed this website? (Okay, I know it was the HackMIT organizers. But if this was a real website, I'd be asking that question.)

## Puzzle 3: `the`

The DeLorean Codes. Okay, this should be fun.

By looking at the source, I found the API endpoint `/api/decode`, which the frontend calls. I pretty quickly made a Python module to call that endpoint. Now, I could play with the reference decoder from the command line, or spam it from Python. Fun stuff.

All you had to do for this puzzle was crack the code. I'll just list the insights I had, in roughly the order I had them.

- Every sample output has a tooltip containing binary. There are five bits in the tooltip per letter in the output. Each letter is associated with a pattern of five bits: a&nbsp;=&nbsp;00000, b&nbsp;=&nbsp;00001, &hellip;&nbsp;, z&nbsp;=&nbsp;11001, space&nbsp;=&nbsp;11010. Bit patterns 11011 to&nbsp;11111 don't mean anything.
- There are as many words in the input as there are letters in the output.
- Refreshing the page reorders the sample input words but doesn't change the sample output. That implies that **the order of the input words doesn't matter**.
- If you take one of the sample inputs and replace one of the words with a word from another sample input, it usually returns ERROR READING. But there's at most one position where it does work. (Sometimes there's no such position when you move a word from a longer sample to a shorter one.) When it does work, it changes one letter in the output, and it changes it to whatever was in that position in the sample that you took the word from. So, **each input word corresponds to a letter and a position**. For a message of length *n* to be valid, there must be one input word corresponding to each position from 0 to&nbsp;*n*&nbsp;&ndash;&nbsp;1. The length of the message doesn't affect what position a word corresponds to.
- I started keeping a log of word meanings that I knew, and couldn't discern a pattern no matter what I did. Also, the words seemed to be all English words, but with some misspellings. I wrote a script, called `attempt_uncover`, to try and decipher a word into its letter and position; plenty of English words translated, but gibberish never did. It seems like there's a **codebook** of some sort&mdash;you can't figure out what a word represents by just doing some computation on the word itself.
- I searched the standard Unix dictionary, `/usr/share/dict/words`, for some of the misspellings, such as `deloreon`. I couldn't find it, even ignoring case and apostrophes. Clearly, the corpus for the codebook isn't the `words` file.
- After using `attempt_uncover` a bunch, I noticed that the words "a better car with price" translated into five adjacent letters in the alphabet, in the same position. Maybe it's drawn in order from a large text corpus? I searched and found [this script for *Back To The Future*](http://www.scifiscripts.com/scripts/backtothefuture_transcript.txt), and tried deciphering a few of the words at the beginning. Bingo: **the codebook is the words of the script of *Back To The Future*, in order, ignoring duplicates** (punctuation is removed and all words are made lowercase). The first word is (0,&nbsp;a), the second word is (0,&nbsp;b), and the 27th unique word is (0,&nbsp;space). Then it skips unique words 28&ndash;32 (remember how every output character translated to a five-bit sequence?), and the 33rd unique word is (1,&nbsp;a).

Using this, I downloaded the script and wrote a program that produced a codebook, then encoded the message by hand. Here was the final ciphertext I sent:

    is a missing can know those around him roster isnt company under struck beer fired confrontations calls met rest einy intact tells vision more radiation aint preserver tab nightmare fiddling john idiots photographic laboratory stuck hospitals interests filthy punk cable asked mad

If only sending things back in time was this easy (or, you know, at all possible).

## Puzzle 4: `hotsinglebots`

Oh, fun, Tinder. An app I've never used, but we'll get by.

As before, the first thing I did was view the page source. I saw comments about `model.json` and `model.hdf5` at the top. Looking at the JSON, it seemed to be referring to some sort of machine learning; the HDF5 I couldn't read, at least in the browser (I Googled it and found it was some sort of binary storage format). I downloaded both and timestamped them, expecting them to change once I'd used the app a bit.

Then, I started swiping. As any dude on Tinder would, I swiped right on every single bot, only to be told "The bot can't see you." The solution was to add a profile picture, which I did, using an old photo from my Facebook profile. Then, I downloaded the model again, just to be safe. It hadn't changed, so I deleted my old copy.

After I added a picture, I started swiping again. This time, the response was "The bot doesn't like you back."

Okay, I can take rejection&hellip;but I have a puzzle to solve, you know?

I decided to take a closer look at the `model` files I downloaded. I wrote a small Python program that loaded the two files, using the `json` and `h5py` libraries, and dropped to a REPL by calling `code.interact`. I looked inside the HDF5; from what I could tell, the file contained weights for some sort of neural network. So the JSON describes the structure of the network, and the HDF5 contains the weights.

That, of course, leaves the question: why is there deep learning on a cheap Tinder clone? The answer was in the JS console; when I tabbed over to it, I was greeted by "Current bot prefers a frog".

Hmm. So maybe the model classifies you into a category, and the bot matches you if your profile picture is in the category it prefers? (I'd also seen people talking about wanting to look like an automobile on the Slack channel, so this somewhat confirmed my suspicions.)

I decided it would probably be useful to be able to run the model locally. I looked up how to load a `model.hdf5` file, and my Googling pointed me to Keras. I downloaded it and wrote a Python program to import the model. (As you can tell, I'm pretty fond of Python. Well, and it's what Keras is written in.)

Next, I needed to know what to feed into the model. I looked at `model.json`, which contains the structure of the model. It seemed to be a sequence of layers, with the first one taking a 32&times;32&times;3 array (presumably a 32&times;32 RGB image) and the last one outputting a vector of size&nbsp;10 (probably a one-hot vector mapping into ten categories). I found the categories defined in one of the `.js` files that the webpage imports, and because everyone on Slack was talking about automobiles, I knew I wanted to maximize index 1 of the array.

The obvious thing to try would be to run the model on every picture I can find. So, I set the model on my entire `~/Pictures` folder.

Not a single one classified as an automobile.

Okay, this is suspicious. Maybe if I find actual pictures of automobiles it will work? I searched the Internet for images of DeLorean cars (going along with the *Back To The Future* theme), picked 20 that seemed legit, and ran them through the classifier. No dice.

Maybe it's some favicon or emoji? A lot of them are 32&times;32. I tried using the custom car emoji from the Slack channel and some favicons from a few websites. Not a single one classified as an automobile. I only gave up when I tried to use the Slack frog emoji, and saw that the standard emoji were all in a spritesheet&mdash;and that none of them were 32&times;32. Reluctantly, I called off my wild goose chase.

At this point, I was stumped. I asked desperately for hints, and eventually figured out that I would need to generate the image somehow instead of finding it somewhere. That led me down a Google rabbit hole with searches like `reverse neural network` and `neural network inverse` and `backwards convolutional neural network` and&hellip;you can see this went nowhere.

Out of desperation, the next thing I tried was *simulated annealing*&mdash;something I'd heard about a fair amount, but never expected to actually have to use. Simulated annealing is an optimization algorithm used to find the minimum or maximum of a function. In this case, I had a 3072-variable function (the neural network, which takes 32&times;32 pixels with 3 channels each), and I wanted to maximize the automobile score. I put together a Python program, with some help from `scipy`, and ran it. But the neural network was taking several seconds for each image, so every iteration of simulated annealing took just as long. After staring at a value that didn't seem to want to creep up past 10<sup>&ndash;9</sup>, I called it off.

Eventually, after more begging for hints, I got the help I needed via Slack DM:

    ameed: and probably without calling the NN too much because slow
    [redacted]: Sure
    [redacted]: Super smart
    ameed: hence no simulated annealing lol
    [redacted]: Correct
    [redacted]: Have you heard about back propagation?
    ameed: Not entirely
    [redacted]: And gradient descent

Hmm. Now we're onto something.

My newfound friend explained what the heck those terms were, and I also looked them up in parallel. But it seemed like they were used more to tune the weights of neural networks, not to invert them:

    [redacted]: You have [to] learn about Keras's APIs
    ameed: lol
    [redacted]: have to
    ameed: it also seems like backpropagation is used to train networks
    ameed: not to optimize inputs
    [redacted]: Right
    [redacted]: But the ideas are similar.

Finally, my contact told me there was a tutorial that would help me. After a bit of Googling, I [found it](https://blog.keras.io/how-convolutional-neural-networks-see-the-world.html). I implemented that with a few modifications (most notably, got rid of the normalization code; I wanted the exact image that classified as an automobile), configured it to print the automobile score after each iteration for debugging, then ran it. At first, the score wasn't high enough, so I bumped up the number of iterations to&nbsp;20000. That was probably too many:

    0.999976
    0.999976
    0.999976
    0.999976
    0.999976
    0.999976
    0.999976
    0.999976
    0.999977
    0.999977
    0.999977
    0.999977

Since I didn't handle the `KeyboardInterrupt` exception, I had to sit there and wait for 20000&nbsp;iterations to go by.

After a really, really long time, it finally spit out an image. I tested it against the model, and finally&mdash;finally&mdash;it said "automobile". Then, all I had to do was set it as my profile picture, and the solution greeted me after another swipe.

Catfishing neural networks is fun.

## Puzzle 5: `captcha`

You don't mean I have to decipher CAPTCHAs myself, right? Oh, you do. Oh, no.

Maybe I shouldn't have dropped that computer vision class.

This time, there wasn't anything incriminating in the webpage source. So, just out of curiosity, I had a look at the `challenge` endpoint, which was where you downloaded the CAPTCHAs from.

Interestingly enough, they seemed to change with every download&mdash;and you only get 1000, a tenth of the minimum you need. Obviously, then, you're supposed to download as many as you need and submit as many as you want, up to the limit of&nbsp;15000. And only 10000 of those have to be correct, so my minimum accuracy rate has to be&nbsp;66.7%.

So, seeing as I couldn't really do much without some CAPTCHAs to crack, I immediately wrote a bit of Python to download a batch and write them out to a folder on my hard drive. When I opened some up, I noticed something strange: the random background was the same for every CAPTCHA! That made things a lot easier&mdash;at least it did when I figured out how to use that knowledge.

Thinking of how much the tutorial helped me out on the previous puzzle, I decided to find a high-level guide to breaking CAPTCHAs. I eventually found [this](https://codepen.io/birjolaxew/post/cracking-captchas-with-neural-networks)&mdash;not precisely what I was looking for, but it would do.

Our first step, then, was to prepare the images. My computer vision class taught me I would want to threshold the images first to turn them into a *binary* format. That means every pixel is either on or off; no grayscale, no colors. That's the first thing the tutorial does, too. (I set my threshold at 128 initially, but later increased it to&nbsp;192 because some adjacent characters were being merged at&nbsp;128.) But unlike in the tutorial, thresholding didn't get rid of all of the noise&mdash;I would need to run an extra step to obliterate the stupid lines.

From what I remembered from computer vision, there are ways to shrink and grow objects in a picture; the effect is to get rid of small features, like the lines, by shrinking them until they disappear, and preserve big ones, like the letters. A bit of Googling revealed what I was looking for: [morphological operators](https://en.wikipedia.org/wiki/Mathematical_morphology#Basic_operators). I used `scipy`'s morphology methods and coded up a simple morphological closing as my first denoise function.

That got rid of almost all the noise, except for a little bit caused by three lines nearly intersecting and creating a bit of an ink blob. Stubborn things. I fixed that by manually overwriting the pixels at the center of that blob, which worked but made a big hole if there happened to be a character in the same place. And I couldn't add any extra dilation to close the holes, or else the stems of the i's would merge with their tittles. (Yes, *tittle* is the actual name for the dot on an i&nbsp;or&nbsp;j.) Oh, well, it would have to do for now.

The next thing the tutorial did was to segment the image into characters to make it easier for the neural network to parse. I could have used `scipy`'s `label` method, but that would separate the i's&nbsp;and&nbsp;j's from their tittles. So, I decided to flatten everything horizontally and segment that. This worked surprisingly well.

Now, I needed some labeled images to use to train the network. I wrote up a Python script called `labelit` that would show me a CAPTCHA and its cleaned, segmented version, then prompt me to decipher it (or mark it `bad` if it was so scrambled that even I couldn't tell what it was). I set it against my downloaded set of samples and labeled a few images, but noticed a problem: my image cleaning was horrible.

Specifically, glyphs were getting mangled by the cleaning process. A lot of&nbsp;e's were turning into&nbsp;c's. I reduced the erosion amount to try and keep the crossbars of the e's alive, but that introduced more artifacts from the lines (since now there were even more intersections that produced large enough blobs to survive erosion). It was becoming obvious that my approach wasn't working. And worse yet, I was being taunted (first in public Slack, then by DM) by people whose cleaning was top-notch already:

    ameed: seems like you've figured out a pretty-good captcha cleaning solution
    ameed: I've been using grey_opening, and manually removing any pixels left over from "hot spots" in the line pattern, but that also tends to screw up everything else
    [redacted]: There's a clever way to remove the lines. Think about the properties the lines have that other parts don't. the method I'm using is entirely done by the computer and pretty fast.
    [redacted]: < 10 lines of python

    (I explain what I've done so far.)

    [redacted]: :)
    [redacted]: I won't say anymore. I'd like a spot :) Your way isn't bad. There's a better one though.
    ameed: Lol, that's sensible XD

At this point, I decided to use one of the few things I could absolutely predict: the layout of the lines. I took 100 thresholded images and multiplied them pointwise by each other, which gave me only the pixels that were on in all&nbsp;100. (I used a lower threshold here than I did for the main cleaning to make sure the lines I captured were broader than any that appeared in actual images. If I used the same threshold, then I might get slightly different results per image, because JPEG artifacts might push certain pixels under or over the threshold. That would mean the lines I captured wouldn't always cover the lines in the CAPTCHAs, and I'd still have artifacts left over.)

Then, for each new image that I preprocessed, I subtracted out the lines. That got rid of the noise pretty easily, but it also left gaps where a line intersected with a letter. I filled the gaps by doing a morphological closing with a large radius, then multiplied that pointwise by the original image so I'd get rid of any artifacts the closing introduced. Finally, I morphologically opened the result with a small radius to try and get rid of any small line fragments that remained.

This was my final denoising code (with the litany of commented-out debugging statements removed):

    def denoise(im):
        ret = np.copy(im)
        ret -= lines.lines * 255
        ret = np.clip(ret, 0, 255)
        ret = scipy.ndimage.grey_closing(ret, (5, 5))
        return scipy.ndimage.grey_opening(ret * im / 255, (2, 2))

It usually produced reasonable results, but didn't always. Most of the bad segmentations were because of some issue with the CAPTCHA, usually characters overlapping or being too close, but sometimes my segmenter assembled things wrong. In one amusing case, there were an h and an&nbsp;m next to each other; the cleaner detached the stem of the m and glued it to the&nbsp;h! But cases like this were rare enough that it didn't mess up my results.

After I rewrote my cleaner, I started labeling a lot of images, for two reasons: (a)&nbsp;I'd need them to train a neural network; (b)&nbsp;someone offered me their cleaning code if I gave them training data. (That never materialized, but it gave me a reason to label bunches of images, which was probably a good thing.) I briefly contemplated churning out 10000&nbsp;labels and solving the problem by hand, but decided against such a masochistic approach. I'm not *that* crazy.

Something key about this problem was that I only had to submit solutions for CAPTCHAs that I *wanted* to solve. That meant if there was some sort of issue with a CAPTCHA, I didn't even have to try and submit a solution! The next step, then, was to figure out the stuff I didn't even want to try and decipher.

So, I wrote a series of sanity checks:

- There are four segments in the image. (Pretty clear, since there are four letters in each CAPTCHA. If there were three or five, I immediately knew that either two letters overlapped or my segmenter broke. That didn't happen often enough for it to be a problem, though&mdash;and even if a bad segmentation produced four segments, usually the other checks caught it.)
- Each segment contains at least&nbsp;53 and at most 205&nbsp;lit pixels. (The lower limit detects cases where a letter is split in two; the stem of an i I measured had 49 pixels. The upper limit throws away any cases of two glyphs being stacked vertically on top of each other and treated as one segment, or of glyphs overlapping; the glyphs I measured had up to 170&nbsp;pixels of area.)
- The bounding box of each segment is at most&nbsp;24&times;24. (This also detects the stacking case.)

Now that I had reasonable-looking cleaned images, I had to do the final task: actually recognize them. Following a suggestion from the Slack channel, my first attempt was with OCR, specifically [Tesseract](https://github.com/tesseract-ocr/tesseract) by Google. I ran it on an entire cleaned CAPTCHA first, but that didn't go too well because the characters weren't horizontally aligned. (For instance, it thought an r above the baseline was an apostrophe.) So, I tried doing it character by character. I wrote a utility to split each segment into a separate array, then ran it through Tesseract.

On the one test case I used, it got zero out of four characters right. That was the end of that; I decided neural networks were a much better choice. I wrote a utility that created 36&nbsp;directories, one for each possible character, and sorted characters into those folders based on the labels I'd assigned them. Then, I manually checked them to make sure they all looked sensible. I was surprised; I could count the number of bad segmentations on one hand!

Now, I needed to figure out how to structure my neural network. I found the [official TensorFlow tutorial](https://www.tensorflow.org/get_started/mnist/beginners) on recognizing MNIST images, and used that for guidance. I adapted it to my case, though, because I wasn't working with MNIST data. Most notably, I changed the input size to&nbsp;24&times;24 (the maximum bounding box that I'd set in my sanity checks), and padded every image to that size before running it through the classifier. Apart from that, I basically followed the tutorial exactly.

I had 1324&nbsp;pre-labeled character images, which I split by the first character of their names: 1122&nbsp;train, 202&nbsp;test. I wrote a program to train a model and export it, then set it to 1000&nbsp;iterations and waited for a few seconds.

    Accuracy: 0.950495

Wait, what? Wow&hellip;neural networks really are that good. Or maybe I've overfit&hellip;

In any event, now was the time to test out my creation. I wrote a Python program to repeatedly download images, sanity-check them, and classify the ones that passed, then POST the result when I got&nbsp;15000. I ran into a few issues (like the one time my program got rate-limited, causing Python `requests` to throw an exception, crash my program, and throw away the 11000&nbsp;CAPTCHAs it had already cracked&hellip;sigh). I also discarded about half the images I downloaded because the sanity checks failed. But eventually, I hit the magic 15000, and was both shocked and relieved to see:

    14998 nj41 37924bf7c0a94715b97577f61a9b1ac6
    14999 xdgb 063b93704c24d7557338db2746c7f065
    15000 3imn 5f0834b0cc9e041a609da67ba77e21e4

    Writing and sending...
    {
      "message": "Congratulations! Marty and Doc are free. You are winrar.",
      "passcode": "[redacted]"
    }

I submitted my solution, and thought there was a glitch when puzzle 6 didn't appear. Then, I refreshed the page:

    CONGRATS! U finished the puzzles. What's your email?

I'd done it.

## Closing thoughts

I was a little shocked that I'd managed to finish everything. I thought there were nine puzzles, because the organizers kept secret how many there actually were. But when I did finish, I was relieved&mdash;both that I'd get a guaranteed HackMIT slot, and that I wouldn't have to invest any more time in the puzzles anymore!

After I finished, I suggested to the organizers that they create a Slack channel for solvers. The next day, I woke up to a bunch of push notifications from a `#solvers` channel, created for the small group of us who'd managed to finish. I'm not going to publish excerpts from that channel, out of respect for its privacy, but I'll say there were a lot of interesting discussions. We shared information on where we were from and what school we attended. We saw graphs of how long people took to solve problems. And we talked about a *lot* of alternative solutions to every challenge. Hopefully some of those solvers will publish how they tackled each of the puzzles.

Overall, I enjoyed this problem set. It was a bit heavy on machine learning, but I was able to get by with what I learned as I solved the problems. I came away feeling just a tiny bit more comfortable with machine learning and programming in general, which is good enough for me.

A few comments on each problem:

1. I thought this was a good entry-level puzzle. Nothing was blatantly easy, nor was it too hard to figure out. I took a bit of a weird approach to cracking the JAR file, but plenty of people used the more reasonable approach of just decompiling, which I think is about the difficulty a first problem should have.
2. This puzzle tickled my security bone, which I always enjoy. There wasn't as much intense security focus as there was on one of last year's problems (which referenced [xkcd&nbsp;327: "Exploits of a Mom"](https://xkcd.com/327/), the famous Little Bobby Tables comic, and involved hacking a larger website). Still, the timing attack was fun, and the insights felt hefty enough to make this a solid second puzzle.
3. This one was interesting, and the cipher was well-designed enough that the insights came at a steady pace that wasn't too fast or too slow. My only complaint is about the reliance on a particular version of the *Back To The Future* script, since the screenplay doesn't seem to be officially published, and especially considering that the puzzle setters said on Slack that they don't like writing puzzles where the answer involves finding a particular search result or dataset. Other than that, though, it was a good problem, and one I enjoyed writing all sorts of tools to solve.
4. I was a bit less pleased with this puzzle. I felt a bit dropped into the deep end at times, especially considering I had to comprehend a sprawling deep learning library *and* figure out neural networks all in one go. It seemed like everyone who didn't know about backpropagation, and specifically the Keras tutorial that basically solved the problem, was stumped until they asked the right person for a hint. The puzzle was also pretty skewed towards people with beefier computers; I heard about people using simulated annealing to solve the problem, even though I abandoned that method because it was too slow. The puzzle wasn't bad&mdash;I did have fun diving into neural networks&mdash;but it wasn't as satisfying as the others.
5. This one felt a lot more interesting. I also used a tutorial, but it wasn't a case of *having* to use one particular tutorial to solve the puzzle. The problem left plenty of avenues open for people to solve. Some people, for instance, used OCR, or ran the entire CAPTCHA through a neural network. Others deciphered the pattern that related a CAPTCHA's name to the letters it contained. And a few poor souls sat down and did it manually. As I wrote my program, I felt like I was crafting my own approach to the puzzle, and I was immensely satisfied when I'd tuned everything successfully to get it to work.

I'm really excited to see how other people approached the problems, and to read anyone else's code that's published on the Internet. And of course, I can't wait for next year's admissions puzzles&mdash;judging by the quality of this year's batch, I know next year's will be a blast.

Meanwhile, I've published most of the workspaces I used to solve the problems. I've omitted certain files, mainly large binaries and files specific to my instance of the puzzle. Anything I've changed from the final state of the filesystem is noted in the README in each folder.

See you at HackMIT 2017!

*Alex*

*This work is licensed under a [Creative Commons 4.0 International License](https://creativecommons.org/licenses/by/4.0/).*
