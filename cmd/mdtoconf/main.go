package main

import (
	"flag"
	"fmt"

	"github.com/example/md-to-confluence/converter"
)

func main() {
	input := flag.String("input", "", "markdown file")
	output := flag.String("output", "", "output docx file")
	flag.Parse()

	if *input == "" || *output == "" {
		flag.Usage()
		return
	}

	out, err := converter.Convert(*input, *output)
	if err != nil {
		fmt.Println("error:", err)
		return
	}
	fmt.Println(out)
}
