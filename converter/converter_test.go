package converter

import (
	"archive/zip"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

func TestConvert(t *testing.T) {
	tmpDir := t.TempDir()
	inputFile := filepath.Join(tmpDir, "in.md")
	outputFile := filepath.Join(tmpDir, "out.docx")
	if err := os.WriteFile(inputFile, []byte("# title"), 0644); err != nil {
		t.Fatal(err)
	}

	runPandoc = func(input, output string) error {
		return os.WriteFile(output, []byte("doc"), 0644)
	}
	runLibreOffice = func(input, outDir string) error {
		docx := filepath.Join(outDir, "temp.docx")
		f, err := os.Create(docx)
		if err != nil {
			return err
		}
		zw := zip.NewWriter(f)
		w, _ := zw.Create("docProps/app.xml")
		w.Write([]byte("<AppVersion>12.0000</AppVersion>"))
		zw.Create("word/document.xml")
		zw.Close()
		f.Close()
		return nil
	}

	result, err := Convert(inputFile, outputFile)
	if err != nil {
		t.Fatal(err)
	}

	r, err := zip.OpenReader(outputFile)
	if err != nil {
		t.Fatal(err)
	}
	defer r.Close()

	var appData []byte
	for _, f := range r.File {
		if f.Name == "docProps/app.xml" {
			rc, _ := f.Open()
			appData, _ = ioutil.ReadAll(rc)
			rc.Close()
		}
	}
	if string(appData) != "<AppVersion>16.0000</AppVersion>" {
		t.Fatalf("unexpected AppVersion: %s", appData)
	}
	if result != outputFile {
		t.Fatalf("expected %s got %s", outputFile, result)
	}
}
