import { AbsoluteFill, staticFile, useVideoConfig } from "remotion";
import { Video } from "@remotion/media";
import { theme } from "./theme";

interface BottleHeroProps {
  videoFile: string;
  trimStartSeconds?: number;
}

export const BottleHero: React.FC<BottleHeroProps> = ({ videoFile, trimStartSeconds = 0 }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      <Video
        src={staticFile(videoFile)}
        muted
        trimBefore={trimStartSeconds * fps}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
        }}
      />
    </AbsoluteFill>
  );
};
