package converter

import (
	"archive/zip"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"

	"github.com/atotto/clipboard"
)

var runPandoc = func(input, output string) error {
	cmd := exec.Command("pandoc", input, "-o", output)
	return cmd.Run()
}

var runLibreOffice = func(input, outDir string) error {
	cmd := exec.Command("libreoffice", "--headless", "--convert-to", "docx", input, "--outdir", outDir)
	return cmd.Run()
}

func setAppVersion(docxFile, version string) error {
	rd, err := zip.OpenReader(docxFile)
	if err != nil {
		return err
	}
	defer rd.Close()

	files := make(map[string][]byte)
	for _, f := range rd.File {
		rc, err := f.Open()
		if err != nil {
			return err
		}
		data, err := ioutil.ReadAll(rc)
		rc.Close()
		if err != nil {
			return err
		}
		files[f.Name] = data
	}

	app := files["docProps/app.xml"]
	if len(app) > 0 {
		re := regexp.MustCompile(`<AppVersion>[^<]*</AppVersion>`)
		repl := []byte("<AppVersion>" + version + "</AppVersion>")
		newText := re.ReplaceAll(app, repl)
		files["docProps/app.xml"] = newText
	}

	tmp := docxFile + ".tmp"
	wz, err := os.Create(tmp)
	if err != nil {
		return err
	}
	zw := zip.NewWriter(wz)
	for name, data := range files {
		w, err := zw.Create(name)
		if err != nil {
			zw.Close()
			wz.Close()
			os.Remove(tmp)
			return err
		}
		_, err = w.Write(data)
		if err != nil {
			zw.Close()
			wz.Close()
			os.Remove(tmp)
			return err
		}
	}
	zw.Close()
	wz.Close()
	err = os.Rename(tmp, docxFile)
	if err != nil {
		return err
	}
	return nil
}

func copyToClipboard(path string) {
	_ = clipboard.WriteAll(path)
}

func Convert(inputPath, outputPath string) (string, error) {
	tmpDir, err := os.MkdirTemp("", "md2conf")
	if err != nil {
		return "", err
	}
	defer os.RemoveAll(tmpDir)

	docFile := filepath.Join(tmpDir, "temp.doc")
	if err := runPandoc(inputPath, docFile); err != nil {
		return "", err
	}

	if err := runLibreOffice(docFile, tmpDir); err != nil {
		return "", err
	}

	docxFile := filepath.Join(tmpDir, "temp.docx")
	if err := os.Rename(docxFile, outputPath); err != nil {
		return "", err
	}

	if err := setAppVersion(outputPath, "16.0000"); err != nil {
		return "", err
	}

	copyToClipboard(outputPath)
	return outputPath, nil
}
