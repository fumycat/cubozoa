use clap::Parser;
use fancy_regex::Regex;
use lazy_static::lazy_static;
use std::fs::File;
use std::io::prelude::*;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(help = "Input file (files)")]
    file: Vec<PathBuf>,
}

lazy_static! {
    static ref RE_DEV: Regex = Regex::new(r"(?:\d\d:){3}[\s\S]*?(?=\n(?:\d\d:){3}|$)").unwrap();
}

fn main() {
    let args = Args::parse();
    for i in args.file {
        println!("i: {}", i.to_str().unwrap())
    }

    // let r = simple_test();
    // match r {
    //     Ok(()) => println!("ok"),
    //     Err(error) => println!("Error {}", error),
    // }
}

fn simple_test() -> std::io::Result<()> {
    let mut file = File::open("example/example.log")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let matches = RE_DEV.find_iter(&contents);

    for elem in matches {
        println!("Match: {}", elem.unwrap().as_str())
    }

    Ok(())
}
