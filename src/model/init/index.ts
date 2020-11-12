
import model from '@/model'
import { registerDocument } from '../actions/editor'

registerDocument(
    model.open_editors[0],
    "inmemory://wut.py",
    "python",
    "wut"
)

registerDocument(
    model.open_editors[0],
    "inmemory://wut2.py",
    "python",
    "wut2"
)

registerDocument(
    model.open_editors[0],
    "inmemory://wut2.sh",
    "shell",
    "#!/usr/bin/env bash\necho 'yay'"
)