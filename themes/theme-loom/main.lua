-- Loom
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "Loom",
        name = "Loom",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x39, 0x30, 0x2A), -- SECONDARY_BGCOLOR
            lcd.RGB(0xE0, 0x86, 0x4A), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6B, 0x65, 0x62), -- DISABLE_COLOR
            lcd.RGB(0x24, 0x1A, 0x13), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xEB, 0xC4, 0xAB), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x10, 0x0C, 0x09), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xC9, 0x8A), -- ACTIVE_COLOR
            lcd.RGB(0x7B, 0x76, 0x74), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xCE, 0x95), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x52, 0x4A, 0x46), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x10, 0x0C, 0x09), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-loom.png", "toolbar-loom-x18.png")),
    })
end

return { init = init }
