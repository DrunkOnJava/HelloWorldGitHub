#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from "@modelcontextprotocol/sdk/types.js";
import { exec } from "child_process";
import { fileURLToPath } from "url";
import path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class ScreenshotServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "screenshot-server",
        version: "0.1.0",
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupToolHandlers();

    this.server.onerror = (error) => console.error("[MCP Error]", error);
    process.on("SIGINT", async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: "take_screenshot",
          description: "Takes a screenshot of a given URL and saves it to the desktop.",
          inputSchema: {
            type: "object",
            properties: {
              url: {
                type: "string",
                description: "The URL of the webpage to capture.",
              },
            },
            required: ["url"],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name !== "take_screenshot") {
        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${request.params.name}`);
      }

      const { url } = request.params.arguments as { url: string };
      const filename = `screenshot-${Date.now()}.png`;
      const outputPath = path.join("/Users/drunkonjava/Desktop", filename);

      return new Promise((resolve, reject) => {
        exec(`screencapture -C -T 2 -o -w ${url} ${outputPath}`, (error, stdout, stderr) => {
          if (error) {
            console.error(`exec error: ${error}`);
            reject(
              new McpError(ErrorCode.InternalError, `Failed to take screenshot: ${error.message}`)
            );
            return;
          }
          if (stderr) {
            console.error(`stderr: ${stderr}`);
            reject(new McpError(ErrorCode.InternalError, `Failed to take screenshot: ${stderr}`));
            return;
          }
          resolve({
            content: [
              {
                type: "text",
                text: `Screenshot saved to ${outputPath}`,
              },
            ],
          });
        });
      });
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Screenshot MCP server running on stdio");
  }
}

const server = new ScreenshotServer();
server.run().catch(console.error);
