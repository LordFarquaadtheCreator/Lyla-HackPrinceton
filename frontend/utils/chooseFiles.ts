import { open } from "@tauri-apps/api/dialog";
import { BaseDirectory, readDir, type FileEntry } from "@tauri-apps/api/fs";

export default async function (mode: "file" | "folder", filterExt: string[]) {
  if (mode === "file") {
    const filePath = (await open({
      filters: [
        {
          name: "Python File",
          extensions: ["py"],
        },
      ],
    })) as string;
    await saveRecentPath(filePath);

    return [filePath];
  }

  // get the folder
  const folderPath = (await open({
    directory: true,
  })) as string;
  const folderEntries = await readDir(folderPath, {
    dir: BaseDirectory.AppData,
    recursive: true,
  });

  // recursively get all flat file paths from the folder
  const processEntries = (entries: FileEntry[]) => {
    const flatFilePaths: string[] = [];

    for (const entry of entries) {
      if (entry.children) {
        const res = processEntries(entry.children);
        flatFilePaths.push(...res);
        continue;
      }

      flatFilePaths.push(entry.path);
    }

    return flatFilePaths;
  };

  await saveRecentPath(folderPath);
  return processEntries(folderEntries);
}
